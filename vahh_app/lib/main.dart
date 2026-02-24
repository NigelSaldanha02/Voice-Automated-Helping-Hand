import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart' as stt;

// 🔴 CHANGE TO YOUR LAPTOP WIFI IP
const String serverUrl = "http://192.168.0.172:5000";

void main() {
  runApp(const VAHHApp());
}

class VAHHApp extends StatelessWidget {
  const VAHHApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomeScreen(),
    );
  }
}

// ======================================================
// HOME SCREEN
// ======================================================

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String displayText = "SPEAK";
  bool busy = false;

  late stt.SpeechToText _speech;

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

  // 🎤 PHONE MICROPHONE STT
 Future<String> listenFromPhone() async {
  bool available = await _speech.initialize();
  if (!available) return "";

  String recognizedText = "";

  await _speech.listen(
    onResult: (result) {
      recognizedText = result.recognizedWords;
    },
    listenOptions: stt.SpeechListenOptions(
      listenMode: stt.ListenMode.confirmation,
      partialResults: false,
    ),
  );

  await Future.delayed(const Duration(seconds: 4));
  await _speech.stop();

  return recognizedText.toLowerCase();
}


  Future<void> runVAHH() async {
    if (busy) return;
    busy = true;

    HapticFeedback.mediumImpact();

    try {
      // 1️⃣ LISTEN (PHONE MIC)
      setState(() => displayText = "Listening...");
      final spokenText = await listenFromPhone();

      if (spokenText.isEmpty) {
        setState(() => displayText = "Didn't catch that");
        await Future.delayed(const Duration(seconds: 2));
        reset();
        return;
      }

      // 2️⃣ YOU SAID
      setState(() => displayText = "You said:\n$spokenText");
      await Future.delayed(const Duration(seconds: 1));

      // 3️⃣ PROCESS COMMAND
      final processRes = await http.post(
        Uri.parse("$serverUrl/process"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"text": spokenText}),
      );

      final result = jsonDecode(processRes.body);

      if (!result["present"]) {
        setState(() => displayText = "Object not present");
        await Future.delayed(const Duration(seconds: 2));
        reset();
        return;
      }

      final String object = result["object"];

      // 4️⃣ SEARCHING
      setState(() => displayText = "Searching for $object...");

      // 5️⃣ POLL YOLO STATUS
      while (true) {
        await Future.delayed(const Duration(seconds: 1));
        final statusRes =
            await http.get(Uri.parse("$serverUrl/status"));
        final state = jsonDecode(statusRes.body)["state"];

        if (state == "detected") {
          HapticFeedback.heavyImpact();
          setState(() => displayText = "Bringing $object...");
        }

        if (state == "done") {
          HapticFeedback.vibrate();
          setState(() =>
              displayText = "✓ ${capitalize(object)} delivered");
          await Future.delayed(const Duration(seconds: 2));
          reset();
          return;
        }
      }
    } catch (_) {
      setState(() => displayText = "Server error");
      await Future.delayed(const Duration(seconds: 2));
      reset();
    }
  }

  void reset() {
    setState(() {
      displayText = "SPEAK";
      busy = false;
    });
  }

  String capitalize(String s) =>
      s[0].toUpperCase() + s.substring(1);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF202020),
      body: SafeArea(
        child: SizedBox(
          width: double.infinity,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 20),

              const Center(
                child: Column(
                  children: [
                    Text("🤖", style: TextStyle(fontSize: 28)),
                    SizedBox(height: 6),
                    Text(
                      "Voice\nAutomated\nHelping\nHand",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        height: 1.25,
                      ),
                    ),
                  ],
                ),
              ),

              const Spacer(),

              Center(
                child: PulsingButton(
                  text: displayText,
                  onTap: runVAHH,
                ),
              ),

              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }
}

// ======================================================
// PULSING BUTTON
// ======================================================

class PulsingButton extends StatefulWidget {
  final String text;
  final VoidCallback onTap;

  const PulsingButton({
    super.key,
    required this.text,
    required this.onTap,
  });

  @override
  State<PulsingButton> createState() => _PulsingButtonState();
}

class _PulsingButtonState extends State<PulsingButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scale;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _scale = Tween(begin: 1.0, end: 1.06).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scale,
      child: GestureDetector(
        onTap: widget.onTap,
        child: Container(
          width: 260,
          height: 260,
          decoration: const BoxDecoration(
            color: Colors.red,
            shape: BoxShape.circle,
          ),
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Text(
                widget.text,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 0.5,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}