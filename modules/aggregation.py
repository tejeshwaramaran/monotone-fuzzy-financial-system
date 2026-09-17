def aggregate_predictions(mfis_down_output: float, mfis_up_output: float, weight_down: float = 0.5, weight_up: float = 0.5) -> float:
    return (weight_down * mfis_down_output) + (weight_up * mfis_up_output)

def linguistic_output(price: float) -> str:
    if price < 100:
        return "Rendah"
    elif price < 150:
        return "Sederhana"
    return "Tinggi"

def explanation_panel(de: float, beta: float, ic: float, prediction: float, label: str) -> str:
    points = []
    if de > 2.0:
        points.append("Debt-to-Equity adalah tinggi, menunjukkan leverage yang tinggi dan menurunkan ramalan harga saham.")
    elif de > 1.0:
        points.append("Debt-to-Equity adalah sederhana, memberi kesan risiko kewangan yang sederhana.")
    else:
        points.append("Debt-to-Equity adalah rendah, menunjukkan risiko leverage yang lebih rendah.")
    if beta > 1.5:
        points.append("Beta adalah tinggi, menunjukkan sensitiviti pasaran yang tinggi dan memberi tekanan kepada ramalan harga saham.")
    elif beta > 1.0:
        points.append("Beta adalah sederhana, menunjukkan pendedahan risiko pasaran yang sederhana.")
    else:
        points.append("Beta adalah rendah, menunjukkan pendedahan risiko pasaran yang lebih rendah.")
    if ic > 20:
        points.append("Interest Coverage adalah tinggi, menunjukkan keupayaan pembayaran faedah yang kukuh dan menyokong ramalan harga saham.")
    elif ic > 8:
        points.append("Interest Coverage adalah sederhana, menunjukkan kedudukan solvency yang sederhana.")
    else:
        points.append("Interest Coverage adalah rendah, menunjukkan keupayaan pembayaran faedah yang lemah.")
    return " ".join(points) + f" Secara keseluruhan, sistem meramalkan harga saham pada tahap {label} dengan nilai RM {prediction:.2f}."
