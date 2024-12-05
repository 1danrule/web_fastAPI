from fastapi import FastAPI, Query

app = FastAPI(
    description='Tour Agency'
)


@app.get('/')
def index():
    return {'status': 200}


@app.get('/offer/details')
def offer_details(information: str = Query("default_info", title='Additional details about the offer',
                                           description='Provide details like tour location or special requests')):
    return {
        'offer_info': information,
        'message': f'You requested details for: {information}'
    }


@app.get('/offer/')
def with_query_param(tour_type: str = Query(title='Type of tour (e.g., adventure, beach, cultural)', default='Write')):
    return {
        'some_information': tour_type,
        'message': f'Filtering tours by type: {tour_type}'
    }
