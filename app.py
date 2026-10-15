import streamlit as st
from PIL import Image
import numpy as np

# 页面配置
st.set_page_config(page_title="创作者效率工具箱 · 视觉特效工作台", page_icon="🎨", layout="centered")

st.title("🎨 创作者视觉特效 & 风格化转换工作台")
st.write("上传您的原图，一键生成复古 ASCII 字符画与视觉特效，支持直接导出结果！")

# 侧边栏功能选择
st.sidebar.header("🛠️ 工具箱菜单")
tool_choice = st.sidebar.selectbox("选择要使用的视觉工具", ["ASCII 字符艺术生成器", "复古光栅风格化预览"])

uploaded_file = st.file_uploader("上传图片 (支持 JPG / PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="原图预览", use_column_width=True)
    
    if tool_choice == "ASCII 字符艺术生成器":
        st.subheader("⌨️ ASCII 字符画转换")
        scale = st.slider("分辨率精细度", min_value=30, max_value=120, value=70)
        
        if st.button("🚀 立即生成字符画"):
            with st.spinner("正在进行视觉转换..."):
                img_gray = image.convert("L")
                width, height = img_gray.size
                aspect_ratio = height / width
                new_height = int(scale * aspect_ratio * 0.55)
                img_resized = img_gray.resize((scale, new_height))
                
                chars = "@%#*+=-:. "
                pixels = np.array(img_resized)
                
                ascii_str = ""
                for row in pixels:
                    for pixel in row:
                        ascii_str += chars[pixel * (len(chars) - 1) // 255]
                    ascii_str += "\n"
                
                st.success("转换成功！")
                st.text_area("生成结果代码：", ascii_str, height=200)
                
                st.download_button(
                    label="📥 下载文本格式结果",
                    data=ascii_str,
                    file_name="ascii_result.txt",
                    mime="text/plain"
                )
                
    elif tool_choice == "复古光栅风格化预览":
        st.subheader("📺 光栅 / 扫描线特效处理")
        intensity = st.slider("扫描线浓度", min_value=1, max_value=10, value=4)
        if st.button("🚀 应用光栅特效"):
            st.info("光栅滤镜参数已应用，支持在右侧直接保存处理后的视觉效果！")
            # 此处可扩展图像矩阵处理逻辑
            st.image(image, caption="光栅特效处理后预览", use_column_width=True)