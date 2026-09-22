import SwiftUI
import CoreMotion

@main
struct VibrationDetectorApp: App {
    var body: some Scene { WindowGroup { ContentView() } }
}

enum Severity: String, Codable { case normal = "Normal", warning = "Warning", critical = "Critical" }

struct DiagnosisResult: Identifiable, Codable {
    let id: UUID
    let date: Date
    let rms: Double
    let frequency: Double
    let component: String
    let severity: Severity
    let recommendations: [String]
}

enum UserTier: String, CaseIterable, Codable {
    case free, lite, pro, premium
    var label: String { rawValue.capitalized }
    var price: String {
        switch self { case .free: return "₹0"; case .lite: return "₹29/mo"; case .pro: return "₹79/mo"; case .premium: return "₹199/mo" }
    }
}

final class VibrationAnalyzer: ObservableObject {
    @Published var isScanning = false
    @Published var progress = 0.0
    @Published var rms = 0.0
    @Published var frequency = 0.0
    @Published var latest: DiagnosisResult?
    @Published var history: [DiagnosisResult] = []
    private let motion = CMMotionManager()
    private var samples: [Double] = []
    private var timer: Timer?
    private let storageKey = "vibration.history"

    init() { loadHistory() }

    func startScan() {
        guard !isScanning, motion.isAccelerometerAvailable else { return }
        samples.removeAll(); progress = 0; isScanning = true
        motion.accelerometerUpdateInterval = 0.01; motion.startAccelerometerUpdates()
        let started = Date()
        timer?.invalidate()
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] timer in
            guard let self else { return }
            if let data = self.motion.accelerometerData {
                let a = data.acceleration
                let magnitude = sqrt(a.x*a.x + a.y*a.y + a.z*a.z)
                self.samples.append(magnitude)
                self.rms = (self.samples.map { $0*$0 }.reduce(0,+) / Double(max(1,self.samples.count))).squareRoot()
                self.frequency = self.estimateFrequency()
            }
            self.progress = min(1, Date().timeIntervalSince(started) / 5.0)
            if self.progress >= 1 { self.stopScan() }
        }
    }

    func stopScan() {
        guard isScanning else { return }
        timer?.invalidate(); timer = nil; motion.stopAccelerometerUpdates(); isScanning = false
        let scaledRMS = rms * 10
        let severity: Severity = scaledRMS > 60 ? .critical : (scaledRMS >= 15 ? .warning : .normal)
        let component = frequency >= 50 && frequency <= 100 ? "AC Compressor" : (frequency >= 10 && frequency < 50 ? "Vehicle Engine" : "General Mechanical")
        let recommendations: [String] = severity == .normal ? ["Normal operation", "Continue routine monitoring"] : (severity == .warning ? ["Schedule maintenance", "Inspect bearings, mounting and alignment"] : ["Stop using the equipment", "Contact a qualified technician immediately"])
        let result = DiagnosisResult(id: UUID(), date: Date(), rms: scaledRMS, frequency: frequency, component: component, severity: severity, recommendations: recommendations)
        latest = result; history.insert(result, at: 0); saveHistory(); progress = 1
    }

    private func estimateFrequency() -> Double {
        guard samples.count > 3 else { return 0 }
        let changes = zip(samples.dropFirst(), samples).filter { ($0-$1)*($0-$1) > 0.01 }.count
        return min(100, Double(changes) / 5.0)
    }
    private func saveHistory() { if let data = try? JSONEncoder().encode(history) { UserDefaults.standard.set(data, forKey: storageKey) } }
    private func loadHistory() { if let data = UserDefaults.standard.data(forKey: storageKey), let saved = try? JSONDecoder().decode([DiagnosisResult].self, from: data) { history = saved } }
}

struct ContentView: View {
    @StateObject private var analyzer = VibrationAnalyzer()
    @AppStorage("user.tier") private var tierRaw = UserTier.free.rawValue
    @State private var showPaywall = false
    private var tier: UserTier { UserTier(rawValue: tierRaw) ?? .free }
    var body: some View {
        TabView {
            ScannerView(analyzer: analyzer, tier: tier, showPaywall: $showPaywall).tabItem { Label("Scanner", systemImage: "waveform.path.ecg") }
            HistoryView(results: analyzer.history).tabItem { Label("History", systemImage: "clock") }
            PlansView(tierRaw: $tierRaw).tabItem { Label("Plans", systemImage: "creditcard") }
        }.sheet(isPresented: $showPaywall) { PaywallView(tierRaw: $tierRaw) }
    }
}

struct ScannerView: View {
    @ObservedObject var analyzer: VibrationAnalyzer; let tier: UserTier; @Binding var showPaywall: Bool
    var body: some View {
        NavigationView { VStack(spacing: 20) {
            Text("Vibration Detector").font(.largeTitle.bold()); Text("Plan: \(tier.label)").foregroundStyle(.secondary)
            ProgressView(value: analyzer.progress).padding(.horizontal)
            HStack { metric("RMS", String(format: "%.1f", analyzer.rms)); metric("Frequency", String(format: "%.1f Hz", analyzer.frequency)) }
            if let result = analyzer.latest { ResultCard(result: result) }
            Button(analyzer.isScanning ? "Stop Scan" : "Start Scan") { if analyzer.isScanning { analyzer.stopScan() } else if tier == .free && analyzer.history.count >= 1 { showPaywall = true } else { analyzer.startScan() } }.buttonStyle(.borderedProminent)
            Spacer()
        }.padding().navigationTitle("Scanner") }
    }
    private func metric(_ title: String, _ value: String) -> some View { VStack { Text(title).font(.caption); Text(value).font(.title2.monospacedDigit()) }.frame(maxWidth: .infinity) }
}

struct ResultCard: View { let result: DiagnosisResult; var body: some View { VStack(alignment: .leading, spacing: 8) { Text(result.severity.rawValue).font(.headline); Text(result.component).font(.subheadline); ForEach(result.recommendations, id: \.self) { Text("• \($0)") } }.frame(maxWidth: .infinity, alignment: .leading).padding().background(.thinMaterial).clipShape(RoundedRectangle(cornerRadius: 12)) } }
struct HistoryView: View { let results: [DiagnosisResult]; var body: some View { NavigationView { List(results) { r in VStack(alignment: .leading) { Text(r.component).font(.headline); Text("\(r.severity.rawValue) · RMS \(String(format: "%.1f", r.rms)) · \(r.date.formatted())").font(.caption) } }.navigationTitle("History") } } }
struct PlansView: View { @Binding var tierRaw: String; var body: some View { NavigationView { List(UserTier.allCases, id: \.self) { plan in HStack { VStack(alignment: .leading) { Text(plan.label).font(.headline); Text(plan.price).foregroundStyle(.secondary) }; Spacer(); Button(tierRaw == plan.rawValue ? "Current" : "Choose") { tierRaw = plan.rawValue }.buttonStyle(.bordered) } }.navigationTitle("Plans") } } }
struct PaywallView: View { @Environment(\.dismiss) private var dismiss; @Binding var tierRaw: String; var body: some View { NavigationView { List([UserTier.lite, .pro, .premium], id: \.self) { plan in Button("\(plan.label) — \(plan.price)") { tierRaw = plan.rawValue; dismiss() } }.navigationTitle("Upgrade to Unlock") } } }
