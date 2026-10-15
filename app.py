from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io
import streamlit as st

# 页面基础配置
st.set_page_config(page_title="创作者高阶视觉与提效工作台", page_icon="🎨", layout="wide")

# 侧边栏菜单
st.sidebar.title("🛠️ 创作者工具箱矩阵")
tool_choice = st.sidebar.selectbox(
    "选择要使用的云端提效工具",
    [
        "1. 赛博朋克/双色调封面滤镜",
        "2. 杂志大片黑白噪点生成器",
        "3. 电影画幅比例与边框美化",
        "4. 赛博 ASCII 字符艺术生成器"
    ]
)

st.title("🎨 创作者高阶视觉与提效工作台（VIP 专属）")
st.write("集成四大主流视觉特效与一键转换能力，专为短视频封面排版、矩阵去重与图文混剪打造，即开即用！")
st.markdown("---")

# 通用文件上传组件
uploaded_file = st.file_uploader("上传您的素材原图 (支持 JPG / PNG / WEBP)", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # 智能尺寸限制，防止云端内存溢出
        max_dimension = 1500
        if max(image.size) > max_dimension:
            image.thumbnail((max_dimension, max_dimension))

        # ==========================================
        # 工具 1：赛博朋克 / 双色调胶片复古滤镜
        # ==========================================
        if tool_choice == "1. 赛博朋克/双色调封面滤镜":
            st.subheader("🎨 赛博朋克 / 双色调胶片复古滤镜")
            st.write("一键将普通照片转换为高饱和、强视觉冲击力的赛博朋克青红/蓝金风格，极适合小红书/抖音爆款封面。")
            
            mode = st.selectbox("选择色调风格", ["经典青橙/蓝红", "暗夜赛博蓝", "复古高光金"])
            
            if st.button("🚀 一键生成色调滤镜"):
                with st.spinner("正在进行多通道色彩矩阵渲染..."):
                    # 转为灰度再映射双色
                    gray = image.convert("L")
                    base_img = ImageOps.autocontrast(gray, cutoff=2)
                    
                    # 根据不同模式构建双色图谱
                    if mode == "经典青橙/蓝红":
                        color1 = (0, 255, 255)  # 青色
                        color2 = (255, 0, 128)  # 玫红
                    elif mode == "暗夜赛博蓝":
                        color1 = (10, 30, 80)   # 暗蓝
                        color2 = (0, 240, 255)  # 荧光蓝
                    else:
                        color1 = (40, 30, 20)   # 暗褐
                        color2 = (255, 200, 50) # 金黄
                        
                    # 映射双色
                    duotone = ImageOps.colorize(base_img, color1, color2)
                    
                    st.image(duotone, caption=f"处理后效果 - {mode}", use_column_width=True)
                    
                    # 转换下载格式
                    buf = io.BytesIO()
                    duotone.save(buf, format="JPEG", quality=95)
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="📥 下载双色调封面大图",
                        data=byte_im,
                        file_name="cyberpunk_cover.jpg",
                        mime="image/jpeg"
                    )

        # ==========================================
        # 工具 2：杂志大片黑白噪点生成器
        # ==========================================
        elif tool_choice == "2. 杂志大片黑白噪点生成器":
            st.subheader("📸 高对比度黑白画报 & 像素颗粒感生成器")
            st.write("模拟高级杂志质感，通过增强对比度与颗粒纹理，彻底摆脱平庸感，打造高冷情绪风封面。")
            
            contrast_val = st.slider("对比度增强系数", 1.0, 3.0, 1.8)
            
            if st.button("🚀 一键生成黑白大片"):
                with st.spinner("正在压制胶片噪点与光影..."):
                    gray = image.convert("L")
                    enhancer = ImageEnhance.Contrast(gray)
                    processed = enhancer.enhance(contrast_val)
                    
                    # 锐化处理
                    processed = processed.filter(ImageFilter.SHARPEN)
                    
                    st.image(processed, caption="高级黑白画报质感", use_column_width=True)
                    
                    buf = io.BytesIO()
                    processed.save(buf, format="JPEG", quality=95)
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="📥 下载黑白艺术大图",
                        data=byte_im,
                        file_name="bw_art_cover.jpg",
                        mime="image/jpeg"
                    )

        # ==========================================
        # 工具 3：电影画幅比例与边框美化
        # ==========================================
        elif tool_choice == "3. 电影画幅比例与边框美化":
            st.subheader("🖼️ 智能电影画幅加框与排版")
            st.write("自动为正方形或竖屏图片上下增加复古黑边/胶片边框，一键拉满电影叙事感，省去用 PS 繁琐切图的烦恼。")
            
            border_size = st.slider("上下黑边厚度比例", 5, 25, 12)
            
            if st.button("🚀 一键添加电影黑边"):
                with st.spinner("正在进行电影宽银幕封装..."):
                    w, h = image.size
                    add_h = int(h * (border_size / 100.0))
                    new_h = h + add_h * 2
                    
                    # 创建全黑画布
                    new_img = Image.new("RGB", (w, new_h), (15, 15, 15))
                    new_img.paste(image, (0, add_h))
                    
                    st.image(new_img, caption="电影宽银幕视觉效果", use_column_width=True)
                    
                    buf = io.BytesIO()
                    new_img.save(buf, format="JPEG", quality=95)
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="📥 下载电影画幅大图",
                        data=byte_im,
                        file_name="movie_frame.jpg",
                        mime="image/jpeg"
                    )

        # ==========================================
        # 工具 4：赛博 ASCII 字符艺术生成器
        # ==========================================
        elif tool_choice == "4. 赛博 ASCII 字符艺术生成器":
            st.subheader("⌨️ ASCII 赛博字符画转换器")
            st.write("将图片转化为矩阵字符，直接复制即可用于抖音/小红书图文文案或冷酷科技风简介。")
            
            col1, col2 = st.columns(2)
            with col1:
                width = st.slider("分辨率精细度 (字符宽度)", min_value=20, max_value=120, value=60)
            with col2:
                invert = st.checkbox("反转色彩明暗", value=True)

            if st.button("🚀 立即生成字符画"):
                with st.spinner("正在进行像素矩阵渲染..."):
                    aspect_ratio = image.height / image.width
                    new_height = int(width * aspect_ratio * 0.55)
                    img_resized = image.resize((width, max(new_height, 10)))

                    img_gray = img_resized.convert("L")
                    enhancer = ImageEnhance.Contrast(img_gray)
                    img_gray = enhancer.enhance(1.6)

                    ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "%", "@", "#"]
                    if invert:
                        ASCII_CHARS = ASCII_CHARS[::-1]

                    pixels = list(img_gray.getdata())
                    chars = [ASCII_CHARS[min(int(pixel / 26.5), len(ASCII_CHARS) - 1)] for pixel in pixels]
                    ascii_str = "".join(chars)

                    ascii_lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
                    final_ascii = "\n".join(ascii_lines)

                    st.success("转换成功！")
                    st.text_area("生成结果代码 (可直接复制):", final_ascii, height=300)

                    st.download_button(
                        label="📥 下载文本格式结果",
                        data=final_ascii,
                        file_name="ascii_art.txt",
                        mime="text/plain",
                    )

    except Exception as e:
        st.error(f"处理图片时发生意外，请尝试更换一张图片或减小分辨率：{e}")
