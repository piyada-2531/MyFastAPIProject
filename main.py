from js import Response

async def on_fetch(request, env):
    # ดึงข้อมูล URL ที่เรียกเข้ามา
    url = request.url
    path = url.split(".workers.dev")[-1] # ดึง Path ต่อท้าย
    
    # 1. หน้าแรก (Home)
    if path == "/" or path == "":
        html = """
        <html>
            <head><meta charset="UTF-8"><title>AK SKY - Home</title></head>
            <body>
                <h1>ยินดีต้อนรับสู่ AK SKY</h1>
                <nav>
                    <a href="/about">เกี่ยวกับเรา</a> | 
                    <a href="/services">บริการ</a> | 
                    <a href="/contact">ติดต่อ</a>
                </nav>
                <hr>
                <h3>รายการที่ต้องทำ (Todo)</h3>
                <p>ระบบ Native Worker กำลังเตรียมการเชื่อมต่อฐานข้อมูลค่ะ</p>
            </body>
        </html>
        """
        return Response.new(html, headers={"content-type": "text/html; charset=utf-8"})

    # 2. หน้า About
    elif "/about" in path:
        return Response.new("<h1>เกี่ยวกับเรา</h1><p>ข้อมูลบริษัท AK SKY</p>", 
                            headers={"content-type": "text/html; charset=utf-8"})

    # 3. หน้า Services
    elif "/services" in path:
        return Response.new("<h1>บริการของเรา</h1><p>รายละเอียดบริการต่างๆ</p>", 
                            headers={"content-type": "text/html; charset=utf-8"})

    # 4. หน้า Contact
    elif "/contact" in path:
        return Response.new("<h1>ติดต่อเรา</h1><p>เบอร์โทรศัพท์: 0xx-xxx-xxxx</p>", 
                            headers={"content-type": "text/html; charset=utf-8"})

    # 5. หน้าอื่นๆ
    else:
        return Response.new("<h1>404 ไม่พบหน้านี้</h1>", status=404, 
                            headers={"content-type": "text/html; charset=utf-8"})