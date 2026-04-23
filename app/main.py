from app.pipelines.pipeline import run_pipeline
from app.pipelines.pdf_pipeline import run_pdf_pipeline

if __name__ == "__main__":
    choice = input("Choose mode: (1) Research Query (2) PDF Upload: ")

    if choice == "1":
        query = input("Enter your research question: ")
        result = run_pipeline(query)

    elif choice == "2":
        file_path = input("Enter PDF file path: ")
        result = run_pdf_pipeline(file_path)

    else:
        print("Invalid choice")
        exit()

    print("\n\n=== FINAL OUTPUT ===\n")
    print(result)
