"""
视频智能抽帧：OpenCV 场景检测 + 返回候选帧位置
混合模式第一步：检测场景大幅变化点，返回 10-15 个候选帧时间戳
"""
import cv2, numpy as np
from typing import List

def detect_scene_changes(video_path: str, min_candidate_frames: int = 10, max_candidate_frames: int = 15) -> List[float]:
    """
    检测视频中画面大幅变化点，返回候选帧时间戳列表（秒）
    使用帧差分法 + 阈值判断
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    frame_diffs = []
    prev_frame = None
    positions = []

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = np.abs(gray.astype(float) - prev_frame.astype(float)).mean()
            frame_diffs.append(diff)
            positions.append(frame_idx / fps)
        prev_frame = gray
        frame_idx += 1

    cap.release()

    if not frame_diffs or min_candidate_frames < 2:
        # 视频太短或参数无效，返回均匀分布的时间点
        return [i * duration / max(1, min_candidate_frames - 1) for i in range(min_candidate_frames)]

    # 计算阈值：使用帧差分的中位数 * 系数
    threshold = np.median(frame_diffs) * 2.5
    change_points = []
    for i, diff in enumerate(frame_diffs):
        if diff > threshold:
            change_points.append(positions[i])

    # 如果变化点太少，使用帧差分峰值补充
    if len(change_points) < min_candidate_frames:
        diff_sorted = sorted(enumerate(frame_diffs), key=lambda x: x[1], reverse=True)
        extra_points = [positions[i] for i, _ in diff_sorted[:min_candidate_frames - len(change_points)]]
        change_points.extend(extra_points)

    # 去重并排序
    change_points = sorted(set(change_points))
    # 确保在视频时间范围内
    change_points = [t for t in change_points if 0 <= t < duration]

    # 均匀采样到 10-15 个
    if len(change_points) > max_candidate_frames:
        indices = np.linspace(0, len(change_points) - 1, max_candidate_frames, dtype=int)
        change_points = [change_points[i] for i in indices]

    # 如果仍然不足，补充均匀分布点
    if len(change_points) < min_candidate_frames:
        gap = duration / (min_candidate_frames - len(change_points) + 1)
        for i in range(1, min_candidate_frames - len(change_points) + 1):
            t = i * gap
            if t not in change_points and t < duration:
                change_points.append(t)

    return sorted(change_points)[:max_candidate_frames]

def extract_frames_at_times(video_path: str, timestamps: List[float], output_dir: str) -> List[str]:
    """
    在指定时间点截取帧图片，返回文件路径列表
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_paths = []

    extracted = 0
    for i, t in enumerate(timestamps):
        target_frame = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = cap.read()
        if ret:
            out_path = os.path.join(output_dir, f"candidate_{i:02d}.jpg")
            cv2.imwrite(out_path, frame)
            frame_paths.append(out_path)
            extracted += 1
        else:
            print(f"Warning: failed to extract frame at t={t:.2f}s")

    print(f"Extracted {extracted}/{len(timestamps)} frames")

    cap.release()
    return frame_paths

if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 2:
        print("Usage: python video_frames.py <video_path>")
        sys.exit(1)
    video_path = sys.argv[1]
    output_dir = os.path.join(os.path.dirname(video_path), "candidates")
    times = detect_scene_changes(video_path)
    print(f"检测到 {len(times)} 个候选帧时间点: {times}")
    paths = extract_frames_at_times(video_path, times, output_dir)
    print(f"已保存到: {paths}")