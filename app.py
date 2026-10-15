from PIL import Image, ImageEnhance
import io
import streamlit as st

st.set_page_config(page_title="创作者视觉特效工作台", page_icon="🎨", layout="wide")

# 侧边栏
st.sidebar.title("🛠️ 工具箱菜单")
tool_choice = st.sidebar.selectbox("选择要使用的视觉工具", ["ASCII 字符艺术生成器"])

st.title("🎨 创作者视觉特效 & 风格化转换工作台")
st.write("上传您的原图，一键生成复古 ASCII 字符画与视觉特效，支持直接导出结果！")

if tool_choice == "ASCII 字符艺术生成器":
    uploaded_file = st.file_uploader(
        "上传图片 (支持 JPG / PNG)", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="原图预览", use_column_width=True)

        st.markdown("---")
        st.subheader("⌨️ ASCII 字符画转换设置")

        col1, col2 = st.columns(2)
        with col1:
            width = st.slider("分辨率精细度", min_value=20, max_value=120, value=60)
        with col2:
            invert = st.checkbox(
                "反转色彩（如果生成的字符太黑/全是@，勾选此项）", value=True
            )

        if st.button("🚀 立即生成字符画"):
            # 1. 调整比例
            aspect_ratio = image.height / image.width
            new_height = int(width * aspect_ratio * 0.55)
            img_resized = image.resize((width, new_height))

            # 2. 转为灰度图并提高对比度
            img_gray = img_resized.convert("L")
            enhancer = ImageEnhance.Contrast(img_gray)
            img_gray = enhancer.enhance(1.5)

            # 3. 字符梯度集（从亮到暗）
            ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "%", "@", "#"]
            if invert:
                ASCII_CHARS = ASCII_CHARS[::-1]

            pixels = img_gray.getdata()
            chars = [ASCII_CHARS[pixel // 26] for pixel in pixels]
            ascii_str = "".join(chars)

            # 4. 格式化排版
            ascii_lines = [
                ascii_str[i : i + width]
                for i in range(0, len(ascii_str), width)
            ]
            final_ascii = "\n".join(ascii_lines)

            st.success("转换成功！")
            st.text_area("生成结果代码:", final_ascii, height=300)

            st.download_button(
                label="📥 下载文本格式结果",
                data=final_ascii,
                file_name="ascii_art.txt",
                mime="text/plain",
            )
