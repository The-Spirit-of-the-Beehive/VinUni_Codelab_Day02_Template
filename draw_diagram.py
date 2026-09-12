import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_workflow():
    fig, ax = plt.subplots(figsize=(15, 6), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")

    # Title & Subtitle
    plt.text(0.5, 0.92, "QUY TRÌNH HIỆN TẠI: ĐIỀU PHỐI SỰ CỐ PIN & CỨU HỘ XANH SM", 
             ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A")
    plt.text(0.5, 0.85, "(Current-State Workflow Mapping — Tổng thời gian: 15 phút/lượt)", 
             ha="center", va="center", fontsize=11, color="#64748B", style="italic")

    # Step specifications
    steps = [
        {
            "num": "Bước 1",
            "title": "Tiếp nhận\ncuộc gọi sự cố",
            "time": "⏱ 2 phút",
            "actor": "Tài xế ➔ Dispatcher",
            "handoff": "🔄 Handoff (Driver/Call)",
            "is_bottleneck": False,
            "in_out": "In: SĐT, Biển số\nOut: Log sự cố"
        },
        {
            "num": "Bước 2",
            "title": "Tra cứu GPS\nvị trí & % pin xe",
            "time": "⏱ 2 phút",
            "actor": "Dispatcher",
            "handoff": "",
            "is_bottleneck": False,
            "in_out": "In: Biển số xe\nOut: Tọa độ, % Pin"
        },
        {
            "num": "Bước 3",
            "title": "Tra cứu trụ sạc\ntrống & cổng tương thích",
            "time": "⏱ 5 phút",
            "actor": "Dispatcher",
            "handoff": "🔴 BOTTLENECK 1",
            "is_bottleneck": True,
            "in_out": "In: GPS, Dòng xe\nOut: Địa chỉ trạm trống"
        },
        {
            "num": "Bước 4",
            "title": "Soạn tin nhắn SMS\nchỉ đường / Cứu hộ",
            "time": "⏱ 5 phút",
            "actor": "Dispatcher",
            "handoff": "🔴 BOTTLENECK 2",
            "is_bottleneck": True,
            "in_out": "In: Dữ liệu trạm sạc\nOut: SMS bản nháp"
        },
        {
            "num": "Bước 5",
            "title": "Duyệt & Gửi tin\nhoặc điều xe cứu hộ",
            "time": "⏱ 1 phút",
            "actor": "Dispatcher ➔ Tài xế",
            "handoff": "🔄 Handoff (SMS/Lệnh)",
            "is_bottleneck": False,
            "in_out": "In: SMS / Lệnh điều xe\nOut: Hoàn tất điều phối"
        }
    ]

    box_width = 0.155
    box_height = 0.42
    y_pos = 0.32
    x_positions = [0.03 + i * 0.195 for i in range(5)]

    for i, s in enumerate(steps):
        x = x_positions[i]
        
        # Border & background styling
        edge_color = "#EF4444" if s["is_bottleneck"] else "#3B82F6"
        fill_color = "#FEF2F2" if s["is_bottleneck"] else "#EFF6FF"
        line_w = 2.0 if s["is_bottleneck"] else 1.5

        # Draw box
        rect = patches.FancyBboxPatch(
            (x, y_pos), box_width, box_height,
            boxstyle="round,pad=0.015,rounding_size=0.02",
            edgecolor=edge_color, facecolor=fill_color, linewidth=line_w
        )
        ax.add_patch(rect)

        # Header tag
        tag_bg = "#EF4444" if s["is_bottleneck"] else "#3B82F6"
        tag_rect = patches.FancyBboxPatch(
            (x + 0.01, y_pos + box_height - 0.05), box_width - 0.02, 0.04,
            boxstyle="round,pad=0.005,rounding_size=0.01",
            edgecolor="none", facecolor=tag_bg
        )
        ax.add_patch(tag_rect)
        ax.text(x + box_width / 2, y_pos + box_height - 0.03, s["num"], 
                ha="center", va="center", fontsize=9, fontweight="bold", color="white")

        # Step Title
        ax.text(x + box_width / 2, y_pos + box_height - 0.12, s["title"], 
                ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1E293B")

        # Time & Actor
        ax.text(x + box_width / 2, y_pos + box_height - 0.21, f"{s['time']}  |  {s['actor']}", 
                ha="center", va="center", fontsize=8, color="#475569", fontweight="semibold")

        # In/Out Data Box
        ax.text(x + box_width / 2, y_pos + box_height - 0.29, s["in_out"], 
                ha="center", va="center", fontsize=7.5, color="#64748B", style="italic")

        # Bottom badge (Handoff or Bottleneck)
        if s["handoff"]:
            badge_color = "#DC2626" if s["is_bottleneck"] else "#0D9488"
            badge_rect = patches.FancyBboxPatch(
                (x + 0.01, y_pos + 0.015), box_width - 0.02, 0.035,
                boxstyle="round,pad=0.005,rounding_size=0.008",
                edgecolor="none", facecolor=badge_color
            )
            ax.add_patch(badge_rect)
            ax.text(x + box_width / 2, y_pos + 0.032, s["handoff"], 
                    ha="center", va="center", fontsize=7.5, fontweight="bold", color="white")

        # Draw connecting arrows between boxes
        if i < 4:
            next_x = x_positions[i+1]
            arrow_start = (x + box_width + 0.005, y_pos + box_height / 2)
            arrow_end = (next_x - 0.005, y_pos + box_height / 2)
            ax.annotate("", xy=arrow_end, xytext=arrow_start,
                        arrowprops=dict(arrowstyle="-|>", color="#94A3B8", lw=2, mutation_scale=15))

    # Legend / Summary box at the bottom
    legend_text = (
        "🔴 Bottlenecks: Bước 3 & Bước 4 chiếm 10/15 phút (Tra cứu đa nền tảng + gõ SMS thủ công, dễ nhầm cổng sạc xe)\n"
        "🔄 Handoffs: Bước 1 (Tài xế ➔ Tổng đài) và Bước 5 (Tổng đài ➔ Tài xế / Xe cứu hộ lưu động)"
    )
    ax.text(0.5, 0.12, legend_text, ha="center", va="center", fontsize=9, color="#334155",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#E2E8F0", edgecolor="#CBD5E1", lw=1))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    output_filename = "04-workflow-diagram.png"
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    print(f"✅ Đã tạo thành công sơ đồ: {output_filename}")

if __name__ == "__main__":
    draw_workflow()