# graphene_flask_example
Graphene/Flask example for Big Mountain Data & Dev 2019 (talk code examples are saved in branch **big_mountain_2019**).
Slides are available on [SlideShare](https://www.slideshare.net/AylaKhan1/build-graphql-apis-with-graphene-big-mountain-data-dev-2019-189172776).

## Python version

Code was tested with Python 3.7.11.

## Build and run

In a venv, virtualenv or conda environment:

```
pip install -r requirements/main_3.7.txt
python app.py
```

Explore data using the GraphiQL IDE by opening 0.0.0.0:5001 in a browser.
Sample queries and mutations are saved in `sample-queries.txt`.

## Testing

Sample tests are included.

```
pip install -r requirements/test_3.7.txt
python setup.py test
```
