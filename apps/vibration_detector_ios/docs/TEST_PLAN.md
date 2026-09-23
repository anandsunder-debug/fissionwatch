# iOS Test Plan — Vibration Detector

Use this checklist before TestFlight/App Store submission.

## Build and permissions
- [ ] Xcode project builds without errors
- [ ] iOS 15+ target
- [ ] `NSMotionUsageDescription` present
- [ ] Launches without crashes

## Scanner
- [ ] Still phone produces Normal result
- [ ] Movement updates RMS and frequency live
- [ ] Stop Scan ends immediately and produces partial-data result
- [ ] Repeated scans complete without crashes

## Freemium UI
- [ ] First free scan allowed
- [ ] Second free scan opens paywall
- [ ] Lite, Pro and Premium selection updates the badge
- [ ] Replace local plan switching with StoreKit 2 before production

## History and UX
- [ ] Results appear newest first
- [ ] Results persist after restart
- [ ] Scanner, History and Plans tabs navigate correctly
- [ ] Dark mode and empty history state work
- [ ] App interruption is handled safely

## Device and release
- [ ] Test on a physical iPhone (simulator has no real vibration input)
- [ ] Validate launch and scan latency
- [ ] Test memory use over multiple scans
- [ ] Add privacy policy, app icon, screenshots and support URL
- [ ] Verify diagnostics against measured reference data; do not treat rule-based outputs as certified fault diagnosis
