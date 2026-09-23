# Vibration Detector — iOS MVP

Separate iOS application directory within FissionWatch.

## Included

- `Sources/VibrationDetectorApp.swift` — SwiftUI app using CoreMotion
- `Package.swift` — Swift Package layout for reuse/distribution
- `docs/` — supplied test plan, quick start, build summary and technical README

## Run in Xcode

1. Create an iOS App project in Xcode using SwiftUI and Swift.
2. Target iOS 15 or later.
3. Add `Sources/VibrationDetectorApp.swift` to the app target.
4. Add `NSMotionUsageDescription` to the target Info.plist.
5. Run on a physical iPhone for accelerometer testing.

## Scope and limitations

This is an MVP reference implementation. Frequency estimation is simplified and diagnostics are rule-based; it is not a validated machine-learning diagnostic system. Subscription buttons are local UI placeholders and must be replaced with StoreKit 2 and App Store Connect products before commercial release.

The app stores scan history locally using UserDefaults. Test the supplied scenarios on a physical device before submission.
