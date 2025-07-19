import streamlit as st
import subprocess
import os
import tempfile

# Path to FFmpeg (Update if needed)
ffmpeg_path = r"C:\Users\karth\Downloads\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"

# UI Setup
st.title("🎞️ Video Enhancer Tool")
st.write("Upload a video to denoise, sharpen, and upscale to your chosen resolution.")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your video file", type=["mp4", "mov", "avi", "mkv"])

# Resolution dropdown
resolution_options = {
    "720p (HD)": (1280, 720),
    "1080p (Full HD)": (1920, 1080),
    "2K": (2560, 1440),
    "4K (Ultra HD)": (3840, 2160),
}
selected_res = st.selectbox("📏 Select output resolution", list(resolution_options.keys()))

# Start processing if a file is uploaded
if uploaded_file is not None:
    if st.button("🚀 Enhance Video"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name

        # Generate output filename
        filename_wo_ext, ext = os.path.splitext(uploaded_file.name)
        enhanced_filename = f"{filename_wo_ext}_enhanced{ext}"
        output_path = os.path.join(tempfile.gettempdir(), enhanced_filename)

        width, height = resolution_options[selected_res]

        # FFmpeg command
        cmd = [
            ffmpeg_path,
            '-y',
            '-i', temp_input_path,
            '-vf', f"hqdn3d=4.0:3.0:6.0:4.5,unsharp=5:5:1.0:5:5:0.0,scale={width}:{height}",
            '-c:v', 'libx264',
            '-preset', 'slow',
            '-crf', '18',
            '-c:a', 'copy',
            output_path
        ]

        st.text("🔧 Processing video...")
        try:
            subprocess.run(cmd, check=True)
            st.success("✅ Done! Download your enhanced video below.")
            with open(output_path, "rb") as file:
                st.download_button("📥 Download Enhanced Video", file, file_name=enhanced_filename)
        except subprocess.CalledProcessError as e:
            st.error("❌ FFmpeg failed. Please check the input file or settings.")
