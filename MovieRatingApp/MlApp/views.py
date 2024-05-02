from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from joblib import load

model = load('./Savedmodel/model.joblib')

def predictor(request):
    return render(request, 'main.html')

def formInfo(request):
    try:
        Movie_year = request.GET['Movie_year']
        Duration = request.GET['Duration']
        Movies_votes = request.GET['Movies_votes']

        # Assuming the values are integers, you might need to convert them
        Movie_year = int(Movie_year)
        Duration = int(Duration)
        Movies_votes = int(Movies_votes)

        y_pred = model.predict([[Movie_year, Duration, Movies_votes]])

        # Get the predicted rating from the model output
        predicted_rating = y_pred[0]

        # Determine if the movie is "Good" or "Bad"
        prediction_result = "Good" if predicted_rating >= 5 else "Bad"

        return render(request, 'result.html', {"predicted_rating": predicted_rating, "prediction_result": prediction_result})

    except MultiValueDictKeyError:
        # Handle the case where one of the keys is missing in the request
        error_message = "Please provide values for 'Movie_year', 'Duration', and 'Movies_votes'."
        return render(request, 'error.html', {"error_message": error_message})
    except ValueError as e:
        # Handle the case where conversion to int fails
        error_message = f"ValueError: {e}"
        return render(request, 'error.html', {"error_message": error_message})
