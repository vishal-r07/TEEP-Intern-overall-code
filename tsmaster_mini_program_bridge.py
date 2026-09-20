import json
import socket
import time


BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 29500
_connection = None
_sent_frames = 0


def _close_connection():
    global _connection
    if _connection is not None:
        try:
            _connection.close()
        except OSError:
            pass
    _connection = None


def forward_to_verifier(can_identifier, data_bytes, timestamp_seconds):
    global _connection, _sent_frames
    packet = {
        "id": f"0x{int(can_identifier):08X}",
        "data": bytes(data_bytes).hex(),
        "timestamp": float(timestamp_seconds),
        "extended": True,
    }
    try:
        if _connection is None:
            _connection = socket.create_connection((BRIDGE_HOST, BRIDGE_PORT), timeout=0.2)
        _connection.sendall((json.dumps(packet) + "\n").encode("utf-8"))
        _sent_frames += 1
        if _sent_frames == 1:
            print("J1939 verifier bridge connected and forwarding CAN frames")
    except OSError as error:
        _close_connection()
        if _sent_frames == 0:
            print(f"J1939 verifier bridge error: {error}")


def on_init():
    print("J1939 verifier bridge loaded")


def on_can_rx(a_can):
    dlc = int(a_can.FDLC)
    data_bytes = bytes(a_can.FData[index] for index in range(dlc))
    forward_to_verifier(a_can.FIdentifier, data_bytes, time.time())


def On_CAN_Rx(a_can):
    on_can_rx(a_can)


def on_stop():
    _close_connection()
