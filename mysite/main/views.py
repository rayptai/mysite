from django.shortcuts import render

from .forms.fruit import FruitForm

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def machine_learning_demo(request):

    if request.method == 'POST':

        # Handle scenario where the form was posted and we want to make a prediction
        form = FruitForm(request.POST)

        # If the user entered invalid data in the form, return the original form instead of a prediction
        if not form.is_valid():
            form = FruitForm()
            context = {
                'form': form,
            }
            return render(request, 'ml/ml.html', context)

        # Extract user inputs from the form data
        mass = form.cleaned_data['mass']
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']

        # Read the data that will be used to train the model from disk
        fruits = pd.read_table('./main/data/fruit_data_with_colors.txt')

        # create a mapping from fruit label value to fruit name to make results easier to interpret
        lookup_fruit_name = dict(zip(fruits.fruit_label.unique(), fruits.fruit_name.unique()))

        # Split the training data into training and validation data
        x = fruits[['mass', 'width', 'height']]
        y = fruits['fruit_label']

        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

        # Create the machine learning classifier that will be trained
        knn = KNeighborsClassifier(n_neighbors=5)

        # Train the classifier
        knn.fit(x_train, y_train)

        # Make a prediction using the trained classifier
        prediction = knn.predict([[mass, width, height]])
        fruit_name = lookup_fruit_name[prediction[0]]

        context = {
            'prediction': fruit_name
        }

        return render(request, "ml/ml_result.html", context)
    else:

        # Handle scenario where the user first hit the page that contains the form
        form = FruitForm()
        context = {
            'form': form,
        }
        return render(request, 'ml/ml.html', context)

