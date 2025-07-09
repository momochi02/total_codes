import subprocess

def capture_screenshot(output_path="screen.png"):
    with open(output_path, 'wb') as f:
        process = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            stdout=f
        )
    print(f"Ảnh màn hình đã lưu tại {output_path}")


def list_connected_devices():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    output = result.stdout.decode()

    lines = output.strip().split('\n')
    devices = []

    for line in lines[1:]:  # Bỏ dòng đầu "List of devices attached"
        if line.strip():
            parts = line.split('\t')
            if len(parts) == 2 and parts[1] == 'device':
                devices.append(parts[0])

    print("📱 Thiết bị đang kết nối:")
    for i, device in enumerate(devices, 1):
        print(f"{i}. {device}")
