import sys, os

# The following is a bit cheeky. This whole thing needs the repository found here https://github.com/tensorflow/models, or specifically
# the slim package found within. This works around having to add that package to the path by checking some common spots first
def import_slim_modules():
    from datasets import imagenet
    from nets import inception
    from preprocessing import inception_preprocessing

try:
    import_slim_modules()
except ImportError:
    # Try find slim relatively, if not then get the user to input it
    abs_path = os.path.abspath(os.path.dirname('../../models/slim/'))
    if os.path.isabs(abs_path):
        sys.path.append(abs_path)
        import_slim_modules()
    else:
        abs_path = input("Slim isn't set on pythons path. Enter the absolute path of Slim to fix this: ")
        sys.path.append(abs_path)
        import_slim_modules()
