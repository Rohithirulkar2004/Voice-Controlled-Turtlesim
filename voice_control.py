import json
import queue
import sys
import os

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import sounddevice as sd
from vosk import Model, KaldiRecognizer


class VoiceControlNode(Node):
    def __init__(self):
        super().__init__('voice_control_node')

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.model_path = os.path.expanduser('~/vosk_models/vosk-model-small-en-us-0.15')

        if not os.path.exists(self.model_path):
            self.get_logger().error(f'Vosk model not found at: {self.model_path}')
            raise FileNotFoundError(f'Vosk model not found at: {self.model_path}')

        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

        self.audio_queue = queue.Queue()
        self.linear_speed = 2.0
        self.angular_speed = 2.0

        self.get_logger().info('Voice control node started')
        self.get_logger().info('Using input device 17')
        self.get_logger().info('Speak: forward, back, left, right, stop, faster, slower')

        self.stream = sd.RawInputStream(
            samplerate=16000,
            blocksize=4000,
            dtype='int16',
            channels=1,
            device=17,
            callback=self.audio_callback
        )
        self.stream.start()

        self.timer = self.create_timer(0.1, self.process_audio)

    def audio_callback(self, indata, frames, time, status):
        if status:
            self.get_logger().warn(f'Audio status: {status}')
        self.audio_queue.put(bytes(indata))

    def process_audio(self):
        while not self.audio_queue.empty():
            data = self.audio_queue.get()
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").lower().strip()
                if text:
                    self.get_logger().info(f'Recognized: {text}')
                    self.execute_command(text)

    def execute_command(self, text):
        msg = Twist()

        if 'forward' in text or text == 'go':
            msg.linear.x = self.linear_speed
            msg.angular.z = 0.0

        elif 'back' in text or 'back' in text:
            msg.linear.x = -self.linear_speed
            msg.angular.z = 0.0

        elif 'left' in text:
            msg.linear.x = 0.0
            msg.angular.z = self.angular_speed

        elif 'right' in text:
            msg.linear.x = 0.0
            msg.angular.z = -self.angular_speed

        elif 'stop' in text:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        elif 'faster' in text:
            self.linear_speed += 0.5
            self.angular_speed += 0.5
            self.get_logger().info(
                f'Speed increased: linear={self.linear_speed}, angular={self.angular_speed}'
            )
            return

        elif 'slower' in text:
            self.linear_speed = max(0.5, self.linear_speed - 0.5)
            self.angular_speed = max(0.5, self.angular_speed - 0.5)
            self.get_logger().info(
                f'Speed decreased: linear={self.linear_speed}, angular={self.angular_speed}'
            )
            return

        else:
            self.get_logger().info(f'Unknown command: {text}')
            return

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Published cmd_vel: linear.x={msg.linear.x}, angular.z={msg.angular.z}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = VoiceControlNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()