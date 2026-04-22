# 🐦 Flappy Bird: Hill Climbing AI Edition

A Flappy Bird clone built using Python and Pygame, featuring an AI-powered autopilot based on the Hill Climbing algorithm for real-time decision-making.

This project demonstrates how local search optimization can be applied in a dynamic, physics-based game environment.

---

## 🚀 Features

* Manual gameplay mode
* AI Autopilot using Hill Climbing
* Smooth physics (gravity, flap, rotation)
* Pixel-perfect collision detection
* Real-time score tracking
* Clean visuals with scrolling background

---

## 🧠 AI Autopilot (Hill Climbing)

The autopilot uses a **greedy local search algorithm** to control the bird.

### How it works:

1. **Target Detection**
   The AI identifies the center of the pipe gap as the target position.

2. **State Evaluation**
   Each frame, the bird’s position is compared with the target.

3. **Decision Making**

   * If the bird is below the target → it flaps
   * If above → no action

4. **Velocity Control**
   The bird only flaps when falling, preventing overshooting and ensuring stable movement.

---

## 🎮 Controls

| Key   | Action             |
| ----- | ------------------ |
| SPACE | Flap (Manual Mode) |
| A     | Toggle Autopilot   |
| M     | Switch Mode        |
| R     | Restart Game       |

---

## 🛠️ Installation & Setup

### Requirements

* Python 3.x
* Pygame

### Steps

```bash
git clone https://github.com/CodeWithFakhir/FlappyBirdGame.git
cd FlappyBirdGame
pip install pygame
python FlappyBirdGame.py
```

---

## 📂 Project Structure

```
Flappy Bird Game/
├── FlappyBirdGame.py
├── Game Assets/
└── README.md
```

---

## 📁 Assets Required

Make sure the **Game Assets/** folder contains:

* background.png
* bird.png
* pipe_top.png
* pipe_bottom.png

---

## 📸 Preview

<img width="2560" height="2560" alt="Game Background" src="https://github.com/user-attachments/assets/c81169cb-2f70-4b9a-9df8-225fd04117eb" />


---

## 🎯 Purpose of the Project

* Demonstrate AI decision-making in games
* Apply search algorithms in real-time systems
* Strengthen Python & Pygame development skills

---

## 👨‍💻 Author

**CodeWithFakhir**
https://github.com/CodeWithFakhir

---

## 📜 License

This project is open-source and available under the MIT License.
