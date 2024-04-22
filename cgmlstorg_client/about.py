# Copyright 2024, Peter van Heusden
#
# This source code is licensed under the MIT License
# found in the LICENSE file in the root directory of this source tree.

# Command line interface for the about() function
# > python -m cgmlstorg_client.about
#
# NB: This module should not be imported by any other code in the package
# (else we will get multiple import warnings)
# Implementation is located in about_.py

if __name__ == "__main__":
    import cgmlstorg_client

    cgmlstorg_client.about()
