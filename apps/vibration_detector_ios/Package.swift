// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "VibrationDetector",
    platforms: [.iOS(.v15)],
    products: [
        .library(name: "VibrationDetector", targets: ["VibrationDetector"])
    ],
    targets: [
        .target(name: "VibrationDetector", path: "Sources")
    ]
)

// Note: SwiftUI @main app targets are normally created and archived through
// an Xcode iOS App project. This manifest provides a package-oriented layout
// for reuse and distribution; create an Xcode app target for App Store builds.
