from setuptools import setup
setup(
    name="Herramientas",
    packages=["herramientas"],
    package_data={"herramientas": ["icons/*.svg"]},
    classifiers=["Example :: Invalid"],
    # Declare orangedemo package to contain widgets for the "Demo" category
    entry_points={"orange.widgets": "Herramientas = herramientas"},
)