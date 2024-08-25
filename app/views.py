from django.http import HttpResponse
from django.shortcuts import render
from model.models import City, TICKET, Stadium
import datetime
import qrcode
# from barcode import generate
from io import BytesIO
def home(request):
    city = City.city_manager.all()
    stadium = Stadium.objects.all()
    date = TICKET.Date
    return render(request, 'index.html', {'city': city, 'stadium': stadium, 'date': date})

def purchase_ticket(request):
    if request.method == 'POST':
        ticket_class = request.POST.get('ticket_class')
        matchname = request.POST.get('matchname')
        date = request.POST.get('date')
        time=request.POST.get('time')
        city=request.POST.get('city')
        stad=request.POST.get('stad')
        price=request.POST.get('price')
        # print(ticket_class," ",matchname," ",date," ",time," ",city," ",stad," ",price)
        return render(request, 'purchase_confirm.html', {
            'ticket_class': ticket_class,
            'matchname': matchname,
            'date': date,
            'time': time,
            'city': city,
            'stad': stad,
            'price': price
        })

def purchase_confirm(request):
    if request.method=='POST': 
        purchase_time = datetime.datetime.now()
        ticket_class = request.POST.get('ticket_class')
        matchname = request.POST.get('matchname')
        date = request.POST.get('date')
        time=request.POST.get('time')
        city=request.POST.get('city')
        stad=request.POST.get('stad')
        price=request.POST.get('price')
        transaction_id = request.POST.get('transaction_id')
        # print(ticket_class," ",matchname," ",date," ",time," ",city," ",stad," ",price," ",transaction_id)
        # form = TicketPurchaseForm(request.POST)
        # if form.is_valid():
        #         transaction_id = form.cleaned_data['transaction_id']
                # ticket_data = {
                #     'ticket_class': form.cleaned_data['ticket_class'],
                #     'matchname': form.cleaned_data['matchname'],
                #     'date': form.cleaned_data['date'],
                #     'time': form.cleaned_data['time'],
                #     'city': form.cleaned_data['city'],
                #     'stad': form.cleaned_data['stad'],
                #     'price': form.cleaned_data['price'],
                #     'transaction_id': form.cleaned_data['transaction_id'],
                # }
                
                # Perform the transaction confirmation logic here, e.g., verify the transaction ID.
                # If the transaction is successful, create the ticket.
        if transaction_successful(transaction_id):
        #    / new_ticket = TicketPurchaseForm.objects.create(**ticket_data)
            # print(ticket_class," ",matchname," ",date," ",time," ",city," ",stad," ",price," ",transaction_id)
            return render(request, 'purchase_success.html' ,{
            'ticket_class': ticket_class,
            'matchname': matchname,
            'date': date,
            'time': time,
            'city': city,
            'stad': stad,
            'price': price,
            'transaction_id':transaction_id,
            'purchase_time':purchase_time
        })
        else:
            return render(request, 'purchase_failed.html')  # Handle failed transaction
    return render(request, 'purchase_confirm.html')

def transaction_successful(transaction_id):
    return bool(transaction_id)

def ticket(request):
    if request.method == 'POST':
        city_name = request.POST.get('city_name')
        stadium_name = request.POST.get('stadium_name')
        match_date = request.POST.get('match_date')
        # Get the actual City and Stadium objects based on the provided names
        try:
            city = City.city_manager.get(name=city_name)
            stadium = Stadium.objects.get(nameofstadium=stadium_name)
        except (City.DoesNotExist, Stadium.DoesNotExist):
            city = None
            stadium = None
        
        # Query the database to check ticket availability
        if city and stadium:
            available_tickets = TICKET.objects.filter(
                city=city,
                stad=stadium,
                Date=match_date,
                is_sold=False
            )
            if available_tickets.exists():
                return render(request, 'ticket.html', {'available_tickets': available_tickets})
            else:
                return render(request, 'not_available.html')
        else:
            # Handle the case where the provided city or stadium name does not exist
            return render(request, 'not_available.html')
    else:
        # If the request method is not POST, render a default template
        return render(request, 'ticket_form.html')
def destination(request):
    if request.method=='POST':
        purchase_time=request.POST.get('purchase_time')
        matchname = request.POST.get('matchname')
        date = request.POST.get('date')
        time=request.POST.get('time')
        print(matchname," ",date," ",time," ",purchase_time)
        barcode_data = f'Match: {matchname}\nDate: {date}\nTime: {time}\nPurchased At: {purchase_time}'

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(barcode_data)
    qr.make(fit=True)

    # Create an in-memory stream for the image
    img_stream = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_stream, format='PNG')
    img_stream.seek(0)

    # Return the image as a response
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'inline; filename="qrcode.png"'
    response.write(img_stream.read())

    return response