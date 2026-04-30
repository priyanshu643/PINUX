#include <Servo.h>

// --- Pin Definitions ---
// Motor Driver L298 Control Pins (Pins 5 to 10) [cite: 7, 42, 43]
#define enA 5
#define in1 6
#define in2 7
#define in3 8
#define in4 9
#define enB 10

// IR Sensors for Line Following [cite: 9, 10, 43, 44]
#define left_IR A0
#define right_IR A1

// Ultrasonic Sensor (HC-SR04) [cite: 11, 12, 44]
#define echoPin A2  // Referred to as "enable pin" in transcript
#define trigPin A3

// Servo Motor [cite: 13, 44]
#define servoPin A5

Servo myServo;

// --- Variables ---
int setpoint = 15; // Stop threshold in cm [cite: 15, 44]
long duration;
int distance_front, distance_left, distance_right;

void setup() {
  Serial.begin(9600); // Initialize Serial Monitor [cite: 17, 45]

  // Initialize Input Pins [cite: 18, 45]
  pinMode(left_IR, INPUT);
  pinMode(right_IR, INPUT);
  pinMode(echoPin, INPUT);

  // Initialize Output Pins [cite: 19, 45, 46, 47]
  pinMode(trigPin, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enB, OUTPUT);

  // Set motor speed to a controlled duty cycle (200 out of 255) [cite: 20, 47, 48]
  analogWrite(enA, 200);
  analogWrite(enB, 200);

  // Servo setup and initial sweep [cite: 21, 48]
  myServo.attach(servoPin);
  myServo.write(140);
  delay(300);
  myServo.write(0);
  delay(300);
  myServo.write(70); // Center position [cite: 30, 59]
  delay(500);

  // Take initial distance reading [cite: 21, 49]
  distance_front = ultra_read();
  delay(500); // Delay before main loop begins [cite: 22, 50]
}

void loop() {
  distance_front = ultra_read(); // Continuously read front distance [cite: 50]

  int left_sensor = digitalRead(left_IR);
  int right_sensor = digitalRead(right_IR);

  // Obstacle detection [cite: 16, 44, 45]
  if (distance_front < setpoint) {
    check_side(); // Stop and scan surroundings [cite: 27, 50, 51]
  } 
  // Line following logic [cite: 24, 25, 51, 52, 53]
  else {
    if (left_sensor == 1 && right_sensor == 1) { // 1 generally means white surface/no line
      forward();
    } else if (left_sensor == 0 && right_sensor == 1) { // 0 means black line detected
      turn_left(); 
    } else if (left_sensor == 1 && right_sensor == 0) {
      turn_right();
    } else {
      stop();
    }
  }
  
  delay(10); // 10-millisecond delay for continuous loop [cite: 23, 53]
}

// --- Custom Functions ---

// Transmit pulse and calculate distance in cm [cite: 26, 53, 54]
int ultra_read() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

// Stop and scan left/right sides for obstacle avoidance [cite: 27, 57]
void check_side() {
  stop();
  delay(100);
  
  myServo.write(140); // Check right side [cite: 28, 57]
  delay(500);
  distance_right = ultra_read();
  Serial.print("Right: ");
  Serial.println(distance_right);

  myServo.write(0); // Check left side [cite: 29, 58, 59]
  delay(500);
  distance_left = ultra_read();
  Serial.print("Left: ");
  Serial.println(distance_left);

  myServo.write(70); // Return to center [cite: 30, 59]
  delay(500);
  compare_distance(); // Determine best path [cite: 30, 59]
}

// Execute bypass sequence based on clearance [cite: 31]
void compare_distance() {
  if (distance_left > distance_right) {
    // Left side has more clearance [cite: 32, 54, 55, 56]
    turn_left();
    delay(500);
    forward();
    delay(600);
    turn_right();
    delay(500);
    forward();
    delay(600);
    turn_right();
    delay(400);
  } else {
    // Right side has more clearance [cite: 33, 56, 57]
    turn_right();
    delay(500);
    forward();
    delay(600);
    turn_left();
    delay(500);
    forward();
    delay(600);
    turn_left();
    delay(400);
  }
}

// --- Motor Movement Functions ---

// Move Forward: clockwise HIGH, anti-clockwise LOW [cite: 34, 59, 60]
void forward() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

// Move Backward: anti-clockwise HIGH, clockwise LOW [cite: 35, 60]
void backward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

// Turn Right: Left motor clockwise, Right motor anti-clockwise [cite: 36, 60]
void turn_right() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

// Turn Left: Left motor anti-clockwise, Right motor clockwise [cite: 37, 60, 61, 62]
void turn_left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

// Stop: All directional motor pins to LOW [cite: 38, 62]
void stop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
