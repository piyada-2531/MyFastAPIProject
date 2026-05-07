from js import Response

async def on_fetch(request, env):
    # ดึงข้อมูล URL ที่เรียกเข้ามา
    url = request.url
    
    # 1. จัดการหน้าแรก (Home /)
    if url.endswith("/") or "index" in url:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>AK SKY - Home</title></head>
        <body>
            <h1>AK SKY (Native Mode)</h1>
            <nav>
                <a href="/about">About</a> | <a href="/services">Services</a> | <a href="/contact">Contact</a>
            </nav>
            <p>ระบบรันผ่าน Native Python Worker สำเร็จแล้วค่ะ</p>
        </body>
        </html>
        """
        return Response.new(html_content, headers={"content-type": "text/html; charset=utf-8"})

    # 2. จัดการหน้า About
    elif "/about" in url:
        return Response.new("<h1>About Page</h1><p>ยินดีต้อนรับสู่หน้าเกี่ยวกับเรา</p>", 
                            headers={"content-type": "text/html; charset=utf-8"})

    # 3. จัดการหน้า Services
    elif "/services" in url:
        return Response.new("<h1>Our Services</h1><p>รายการบริการของเรา</p>", 
                            headers={"content-type": "text/html; charset=utf-8"})

    # 4. จัดการหน้า Contact
    elif "/contact" in url:
        return Response.new("<h1>Contact Us</h1><p>ช่องทางการติดต่อ</p>", 
                            headers={"content-type": "text/html; charset=utf-8"})

    # กรณีหาหน้าไม่เจอ
    return Response.new("404 Not Found", status=404)