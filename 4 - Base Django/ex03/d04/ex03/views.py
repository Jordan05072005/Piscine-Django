from django.shortcuts import render

# Create your views here.

def index(request):
    rows = []
    n = 50
    for i in range(n):
        v = round(i * 200 / (n - 1)) #255
        rows.append({
            "col1":  f"#{v:02X}{v:02X}{v:02X}",
            "col2": f"#{v:02X}0000",
            "col3":  f"#0000{v:02X}",
            "col4":  f"#00{v:02X}00",
        })
    return render(request, "index.html", {'rows': rows})
# for i in range(1, 11)