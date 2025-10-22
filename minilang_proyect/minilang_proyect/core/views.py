from django.shortcuts import render

def index(request):
    resultado_expr = None
    resultado_suma = None
    x_val = request.POST.get('x', '')
    y_val = request.POST.get('y', '')

    if request.method == "POST":
        try:
            x = int(x_val)
            y = int(y_val)

            # Cálculos
            resultado_expr = x * y + 10
            resultado_suma = x + 1

        except ValueError:
            resultado_expr = "Error: Ingresa números válidos"
            resultado_suma = "—"

    context = {
        'x': x_val,
        'y': y_val,
        'resultado_expr': resultado_expr,
        'resultado_suma': resultado_suma
    }

    return render(request, 'core/index.html', context)