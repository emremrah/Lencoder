# Lencoder (Label encoder)

### You can:

* Fit a data-encoder to initiate an encoder. The encoder will be saved as a pickle file.
* Update a previously saved encoder with newcomer data
* Transform and inverse transform your newcomer data

### Constraints:
* Data only can be retrieved as `pandas.Series` for now. Improvements will be made.
* Encoders are going to be saved as `pickle` files to given directory. Improvements can be made.