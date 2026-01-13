# 🦾 ﻿Voice-Automated-Helping-Hand-using-Object-Detection

## 📌 Overview  
This project aims to develop a **voice-controlled robotic assistant** capable of recognizing and retrieving household objects. It combines **speech recognition, object detection, kinematics, and robotic control** to create a “Helping Hand” for elderly individuals and people with mobility challenges.  

The system integrates:  
- **Voice automation** (speech-to-text)  
- **YOLO-based object detection** with dual-camera setup  
- **Kinematic modeling** for robotic arm movement  
- **Mobile app interface** for user commands  
- **Raspberry Pi + ESP32 hardware control**  

---

## 🎯 Objectives  
- Enable **natural voice interaction** with the robot  
- Detect and localize household objects using **computer vision**  
- Implement **inverse kinematics** for accurate arm control  
- Build a **modular system** that integrates software + hardware seamlessly  

---

## 🏗️ System Architecture  

### Hardware  
- **Raspberry Pi** → main controller for object detection & voice processing  
- **ESP32** → robotic arm control + actuation  
- **Dual Cameras**:  
  - Overhead camera → XY coordinate localization of objects  
  - Arm-mounted camera → classification & confirmation  
- **Robotic Arm** → executes pick-and-place tasks  

### Software  
- **Speech Recognition**: Google API / Vosk / Whisper    
- **Object Detection**: YOLO  
- **Mobile App**: Flutter / Flask backend (or MIT App Inventor for prototype)  

---

## 📚 Literature Review Summary  
We reviewed **15 research papers** covering:  
- Object detection techniques (YOLO)  
- Speech recognition models (Vosk, Whisper, SpeechRecognition, PocketSphinx)  
- Kinematics in robotic manipulators  
- Assistive robotics applications  

**Key Takeaways:**  
- YOLO is widely used for real-time household object detection  
- Whisper and Vosk provide offline/on-device STT, while Google API is cloud-based  
- Kinematics formulas are essential for robotic arm accuracy  
- Prior works lacked full integration of **voice + vision + robotics** in a single system — this is our innovation point  

---

## 📅 Project Timeline  

**Sept – Dec 2025:**  
- ✅ Literature Review (Sept–Oct)  
- ✅ Finalize STT  
- ✅ Implement object detection
- ✅ Build simple mobile app interface  

**Jan – Apr 2026:**  
- 🔄 Develop robotic arm kinematics & simulations  
- 🔄 Integrate vision, voice, and arm control  
- 🔄 Build first working prototype  
- 🔄 Fine-tuning and improvements  

---

## 📌 Current Status  
- ✅ Literature review completed  
- 🔄 Exploring STT frameworks (Google API, Vosk, Whisper)  
- 🔄 Testing YOLO for household object detection  
- 🔄 Designing system workflow and block diagrams  

---

## 🚀 Future Scope  
- Expand object database for detection  
- Improve arm precision with advanced kinematics  
- Enable multi-object tasks (e.g., fetch + deliver sequence)  
- Add haptic/safety features  

---

## 📖 References  
- Nantzios, G.; Baras, N.; Dasygenis, M. Design and Implementation of a Robotic Arm Assistant with Voice Interaction Using Machine Vision. Automation 2021, 2, 238-251. https://doi.org/10.3390/automation2040015
- B. Balakrishnan, R. Chelliah, M. Venkatesan and C. Sah, "Comparative Study On Various Architectures Of Yolo Models Used In Object Recognition," 2022 International Conference on Computing, Communication, and Intelligent Systems (ICCCIS), Greater Noida, India, 2022, pp. 685-690, doi: 10.1109/ICCCIS56430.2022.10037635. keywords: {Industries;Deep learning;Computational modeling;Object detection;Computer architecture;Classification algorithms;Object recognition;YOLO;SSD;Fast R-CNN;Faster R-CNN;HOG;Deep Learning;Object Detection}
- J. U.K., I. V., K. J. Ananthakrishnan, K. Amith, P. S. Reddy and P. S., "Voice Controlled Personal Assistant Robot for Elderly People," 2020 5th International Conference on Communication and Electronics Systems (ICCES), Coimbatore, India, 2020, pp. 269-274, doi: 10.1109/ICCES48766.2020.9138101. keywords: {Bluetooth;Service robots;Robot vision systems;Object detection;Manipulators;Cameras;Mobile robots;Object recognition;Older adults;Robots;wheeled mobile robot(WMR);robotic arm;object detection;distance measurement;voice control;personal assistance},
- D. A. Jimenez-Nixon, M. C. Paredes-Sánchez and A. M. Reyes-Duke, "Design, construction and control of a SCARA robot prototype with 5 DOF," 2022 IEEE International Conference on Machine Learning and Applied Network Technologies (ICMLANT), Soyapango, El Salvador, 2022, pp. 1-6, doi: 10.1109/ICMLANT56191.2022.9996479. keywords: {Additives;Service robots;Prototypes;Kinematics;Machine learning;Programming;Software;five degrees of freedom;prototype;SCARA;robotic design;robotics;robots;industry 4.0},
- Y. A. Wubet and K. -Y. Lian, "Voice Conversion Based Augmentation and a Hybrid CNN-LSTM Model for Improving Speaker-Independent Keyword Recognition on Limited Datasets," in IEEE Access, vol. 10, pp. 89170-89180, 2022, doi: 10.1109/ACCESS.2022.3200479.
keywords: {Speech recognition;Convolutional neural networks;Data models;Training data;Mel frequency cepstral coefficient;Linguistics;CNN-LSTM;data augmentation;speaker-independent keyword recognition;voice conversion},
- L. B. Duc, M. Syaifuddin, T. T. Toai, N. H. Tan, M. N. Saad and L. C. Wai, "Designing 8 Degrees of Freedom Humanoid Robotic Arm," 2007 International Conference on Intelligent and Advanced Systems, Kuala Lumpur, Malaysia, 2007, pp. 1069-1074, doi: 10.1109/ICIAS.2007.4658549. keywords: {Artificial intelligence;Conferences;humanoid robotics;multi degree of freedom;microcontroller;motion control},
- R. A. John, S. Varghese, S. T. Shaji and K. M. Sagayam, "Assistive Device for Physically Challenged Persons Using Voice Controlled Intelligent Robotic Arm," 2020 6th International Conference on Advanced Computing and Communication Systems (ICACCS), Coimbatore, India, 2020, pp. 806-810, doi: 10.1109/ICACCS48705.2020.9074236. keywords: {Manipulators;Speech recognition;Servomotors;Prototypes;Rails;Robot sensing systems;Raspberry pi;voice recognition module;robotic arm},
- Panicker, John & Jain, Divy & N, Vibodh & Yeshwanth, T. & Ramaiah, Swetha. (2023). SwabBot-An oral Swabbing Robotic arm. 1-6. 10.1109/ICECCME57830.2023.10252564.
- J. Nannda, L. V. Dora, T. Gupta, A. Chouhan and A. Verma, "A Robotic Arm Vehicle using Voice Recognition for Physically Challenged People," 2024 2nd International Conference on Advances in Computation, Communication and Information Technology (ICAICCIT), Faridabad, India, 2024, pp. 858-862, doi: 10.1109/ICAICCIT64383.2024.10912202. keywords: {Microcontrollers;Speech recognition;Medical services;Grasping;Assistive technologies;Manipulators;Information and communication technology;Artificial intelligence;Robotic Vehicle;Voice recognition;Microcontroller;pick;place;Arm},
- K. Kawamura and M. Iskarous, "Trends in service robots for the disabled and the elderly," Proceedings of IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS'94), Munich, Germany, 1994, pp. 1647-1654 vol.3, doi: 10.1109/IROS.1994.407636. keywords: {Service robots;Senior citizens;Intelligent robots;Mobile robots;Intelligent systems;Laboratories;Medical robotics;Hardware;Research and development;Safety},
- S. Rafsan, S. Arefin, A. H. M. M. R. Hasan and M. M. Hoque, "Design a human-robot interaction framework to detect household objects," 2016 5th International Conference on Informatics, Electronics and Vision (ICIEV), Dhaka, Bangladesh, 2016, pp. 973-978, doi: 10.1109/ICIEV.2016.7760144. keywords: {Image color analysis;Color;Robots;Object detection;Human-robot interaction;Glass;Object recognition;Human-robot interaction;interactive object detetction;object recognition;classification;evaluation},
- B. Karthika, M. Dharssinee, V. Reshma, R. Venkatesan and R. Sujarani, "Object Detection Using YOLO-V8," 2024 15th International Conference on Computing Communication and Networking Technologies (ICCCNT), Kamand, India, 2024, pp. 1-4, doi: 10.1109/ICCCNT61001.2024.10724411. keywords: {YOLO;Visualization;Accuracy;Webcams;Heuristic algorithms;Surveillance;Classification algorithms;Object recognition;Vehicle dynamics;Videos;Object detection;YOLO;Dynamic object tracking;Visual data;Classification;Recognition},
- R. K. Megalingam, R. S. Reddy, Y. Jahnavi and M. Motheram, "ROS Based Control of Robot Using Voice Recognition," 2019 Third International Conference on Inventive Systems and Control (ICISC), Coimbatore, India, 2019, pp. 501-507, doi: 10.1109/ICISC44355.2019.9036443. keywords: {Hidden Markov models;Speech recognition;Software;DC motors;Robot kinematics;Mobile robots;voice-controlled robot;Pocket Sphinx;voice recognition;ROS},
- S. F. Ahmed, R. Jaffari, M. Jawaid, S. S. Ahmed and S. Talpur, "An MFCC-based Secure Framework for Voice Assistant Systems," 2022 International Conference on Cyber Warfare and Security (ICCWS), Islamabad, Pakistan, 2022, pp. 57-61, doi: 10.1109/ICCWS56285.2022.9998446. keywords: {Performance evaluation;Home automation;Navigation;Authentication;Speech recognition;Temperature control;Security;voice recognition;voice assistant;security;MFCC;cross-platform},
- Al Tahtawi, Adnan & Agni, Muhammad & Hendrawati, Trisiani. (2021). Small-scale Robot Arm Design with Pick and Place Mission Based on Inverse Kinematics. Journal of Robotics and Control (JRC). 2. 10.18196/26124. 

---


