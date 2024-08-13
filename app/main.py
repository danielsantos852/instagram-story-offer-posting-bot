# --- Imports ---

# Local
from pipeline import Pipeline


# --- Main Function ---

def main():

    # Get pipeline
    pipeline = Pipeline.get()

    # Run pipeline
    pipeline.run()


# Call main()
if __name__=='__main__': main()