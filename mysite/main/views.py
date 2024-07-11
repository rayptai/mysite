from django.shortcuts import render

from .forms.fruit import FruitForm

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def machine_learning_demo(request):
    if request.method == 'POST':
        form = FruitForm(request.POST)

        if not form.is_valid():
            form = FruitForm()
            context = {
                'form': form,
            }
            return render(request, 'ml/ml.html', context)

        mass = form.cleaned_data['mass']
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']

        fruits = pd.read_table('./main/data/fruit_data_with_colors.txt')

        # create a mapping from fruit label value to fruit name to make results easier to interpret
        lookup_fruit_name = dict(zip(fruits.fruit_label.unique(), fruits.fruit_name.unique()))

        x = fruits[['mass', 'width', 'height']]
        y = fruits['fruit_label']

        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(x_train, y_train)

        prediction = knn.predict([[mass, width, height]])
        fruit_name = lookup_fruit_name[prediction[0]]

        context = {
            'prediction': fruit_name
        }

        return render(request, "ml/ml_result.html", context)
    else:
        form = FruitForm()
        context = {
            'form': form,
        }
        return render(request, 'ml/ml.html', context)

