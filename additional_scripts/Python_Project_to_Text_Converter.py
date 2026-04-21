import os
import shutil

def convert_py_to_txt(source_dir, output_dir):
    # Jeśli folder istnieje, usuwamy go wraz z zawartością
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Stary folder {output_dir} został usunięty.")

    # Teraz tworzymy go na nowo (pusty)
    os.makedirs(output_dir)
    print(f"Utworzono świeży folder: {output_dir}")
            
    # Przeszukujemy drzewo katalogów
    for root, dirs, files in os.walk(source_dir):
        # Omijamy foldery, których nie chcemy w NotebookLM (np. biblioteki lub migracje)
        if 'venv' in root or '__pycache__' in root or '.git' in root or 'migrations' in root:
            continue
            
        for file in files:
            if file.endswith(".py") or file.endswith(".html"):
                # Budujemy pełną ścieżkę do pliku źródłowego
                file_path = os.path.join(root, file)
                
                # Tworzymy unikalną nazwę dla pliku .txt, zamieniając ścieżkę na nazwę
                # np. blog/views.py stanie się blog_views.txt
                # Rozdzielamy ścieżkę na nazwę bez rozszerzenia i samo rozszerzenie
                relative_path = os.path.relpath(file_path, source_dir)
                base_path, _ = os.path.splitext(relative_path)

                # Zamieniamy separatory folderów na podkreślniki i dodajemy .txt
                new_filename = base_path.replace(os.sep, "_") + ".txt"
                
                target_path = os.path.join(output_dir, new_filename)
                
                # Kopiujemy zawartość
                shutil.copy2(file_path, target_path)
                print(f"Skonwertowano: {file} -> {new_filename}")

# Użycie:
# source = "." oznacza bieżący folder, w którym jest skrypt
# output = "project_docs" to folder, który potem wrzucisz do NotebookLM
convert_py_to_txt(".", "project_docs")