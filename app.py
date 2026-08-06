# tkinter creates the application window
import tkinter as tk
from tkinter import ttk, messagebox

# sqlite3 connects to the manga database
import sqlite3
from pathlib import Path


# database location
database_file = Path("manga.db")


# main colours
background_colour = "#090909"
panel_colour = "#151515"
panel_hover_colour = "#202020"

orange_colour = "#ff6a00"
orange_hover_colour = "#ff8533"
orange_dark_colour = "#8f3b00"

text_colour = "#f5f5f5"
muted_text_colour = "#a8a8a8"
border_colour = "#333333"


# clear the current table results
def clear_table():
    for item in results_table.get_children():
        results_table.delete(item)


# run an sql query and display the results
def run_query(query, heading):
    if not database_file.exists():
        messagebox.showerror(
            "database error",
            "manga.db was not found"
        )
        return

    try:
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()

        cursor.execute(query)

        # get the column names
        column_names = [
            description[0]
            for description in cursor.description
        ]

        rows = cursor.fetchall()

        connection.close()

        clear_table()

        # update the table columns
        results_table["columns"] = column_names
        results_table["show"] = "headings"

        for column in column_names:
            display_name = column.replace("_", " ").title()

            results_table.heading(
                column,
                text=display_name
            )

            results_table.column(
                column,
                width=170,
                minwidth=120,
                anchor="center"
            )

        # add every returned row
        for row in rows:
            results_table.insert(
                "",
                "end",
                values=row
            )

        current_query_label.config(text=heading)

        result_count_label.config(
            text=f"{len(rows)} result(s) found"
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "database error",
            str(error)
        )


# show every manga
def show_all_manga():
    query = """
        select
            manga.title,
            authors.author_name,
            manga.release_year,
            manga.publication_status,
            reading_progress.rating
        from manga
        join authors
            on manga.author_id = authors.author_id
        join reading_progress
            on manga.manga_id = reading_progress.manga_id
        order by manga.title;
    """

    run_query(query, "all manga")


# show manga currently being read
def show_reading():
    query = """
        select
            manga.title,
            reading_progress.current_volume,
            reading_progress.volumes_owned,
            reading_progress.rating
        from manga
        join reading_progress
            on manga.manga_id = reading_progress.manga_id
        where reading_progress.reading_status = 'Reading'
        order by reading_progress.rating desc;
    """

    run_query(query, "currently reading")


# show completed manga
def show_completed():
    query = """
        select
            manga.title,
            authors.author_name,
            manga.total_volumes,
            reading_progress.rating
        from manga
        join authors
            on manga.author_id = authors.author_id
        join reading_progress
            on manga.manga_id = reading_progress.manga_id
        where reading_progress.reading_status = 'Completed'
        order by reading_progress.rating desc;
    """

    run_query(query, "completed manga")


# show favourite manga
def show_favourites():
    query = """
        select
            manga.title,
            authors.author_name,
            reading_progress.rating,
            reading_progress.notes
        from manga
        join authors
            on manga.author_id = authors.author_id
        join reading_progress
            on manga.manga_id = reading_progress.manga_id
        where reading_progress.favourite = 1
        order by reading_progress.rating desc;
    """

    run_query(query, "favourites")


# show highly rated manga
def show_high_rated():
    query = """
        select
            manga.title,
            reading_progress.rating,
            reading_progress.reading_status
        from manga
        join reading_progress
            on manga.manga_id = reading_progress.manga_id
        where reading_progress.rating >= 8.5
        order by reading_progress.rating desc;
    """

    run_query(query, "rated 8.5 or higher")


# create a styled query button
def create_query_button(parent, text, command, column):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        foreground=text_colour,
        background=panel_hover_colour,
        activeforeground="#000000",
        activebackground=orange_hover_colour,
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=18,
        pady=11
    )

    button.grid(
        row=0,
        column=column,
        padx=6,
        pady=6,
        sticky="ew"
    )

    # make the button orange when hovered
    button.bind(
        "<Enter>",
        lambda event: button.config(
            background=orange_colour,
            foreground="#000000"
        )
    )

    # return to dark when the mouse leaves
    button.bind(
        "<Leave>",
        lambda event: button.config(
            background=panel_hover_colour,
            foreground=text_colour
        )
    )

    return button


# create the application window
window = tk.Tk()

window.title("MangaVault")
window.geometry("1150x700")
window.minsize(900, 550)
window.configure(background=background_colour)


# style the tkinter table
style = ttk.Style()

style.theme_use("clam")


# table background
style.configure(
    "Manga.Treeview",
    background=panel_colour,
    foreground=text_colour,
    fieldbackground=panel_colour,
    borderwidth=0,
    rowheight=38,
    font=("Segoe UI", 10)
)


# selected table row
style.map(
    "Manga.Treeview",
    background=[
        ("selected", orange_dark_colour)
    ],
    foreground=[
        ("selected", "#ffffff")
    ]
)


# table column headings
style.configure(
    "Manga.Treeview.Heading",
    background=orange_colour,
    foreground="#000000",
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 10, "bold"),
    padding=10
)


# heading hover colour
style.map(
    "Manga.Treeview.Heading",
    background=[
        ("active", orange_hover_colour)
    ]
)


# scrollbar style
style.configure(
    "Vertical.TScrollbar",
    background=orange_colour,
    troughcolor=panel_colour,
    bordercolor=panel_colour,
    arrowcolor=text_colour
)


style.configure(
    "Horizontal.TScrollbar",
    background=orange_colour,
    troughcolor=panel_colour,
    bordercolor=panel_colour,
    arrowcolor=text_colour
)


# orange line across the top
top_accent = tk.Frame(
    window,
    background=orange_colour,
    height=6
)

top_accent.pack(
    fill="x"
)


# main page container
main_container = tk.Frame(
    window,
    background=background_colour
)

main_container.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=25
)


# application header
header_frame = tk.Frame(
    main_container,
    background=background_colour
)

header_frame.pack(
    fill="x",
    pady=(0, 22)
)


# small orange logo block
logo_frame = tk.Frame(
    header_frame,
    background=orange_colour,
    width=58,
    height=58
)

logo_frame.pack(
    side="left",
    padx=(0, 16)
)

logo_frame.pack_propagate(False)


logo_label = tk.Label(
    logo_frame,
    text="MV",
    font=("Segoe UI", 17, "bold"),
    foreground="#000000",
    background=orange_colour
)

logo_label.pack(
    expand=True
)


# title section
title_frame = tk.Frame(
    header_frame,
    background=background_colour
)

title_frame.pack(
    side="left"
)


title_label = tk.Label(
    title_frame,
    text="MangaVault",
    font=("Segoe UI", 27, "bold"),
    foreground=text_colour,
    background=background_colour
)

title_label.pack(
    anchor="w"
)


subtitle_label = tk.Label(
    title_frame,
    text="manga collection and reading database",
    font=("Segoe UI", 10),
    foreground=muted_text_colour,
    background=background_colour
)

subtitle_label.pack(
    anchor="w",
    pady=(2, 0)
)


# orange divider beneath the header
header_line = tk.Frame(
    main_container,
    background=orange_dark_colour,
    height=2
)

header_line.pack(
    fill="x",
    pady=(0, 20)
)


# query controls card
controls_frame = tk.Frame(
    main_container,
    background=panel_colour,
    highlightbackground=border_colour,
    highlightthickness=1
)

controls_frame.pack(
    fill="x",
    pady=(0, 18)
)


controls_inner = tk.Frame(
    controls_frame,
    background=panel_colour
)

controls_inner.pack(
    fill="x",
    padx=15,
    pady=14
)


query_label = tk.Label(
    controls_inner,
    text="QUERY DATABASE",
    font=("Segoe UI", 9, "bold"),
    foreground=orange_colour,
    background=panel_colour
)

query_label.pack(
    anchor="w",
    padx=6,
    pady=(0, 8)
)


button_frame = tk.Frame(
    controls_inner,
    background=panel_colour
)

button_frame.pack(
    fill="x"
)


# make each button column equal width
for column_number in range(5):
    button_frame.columnconfigure(
        column_number,
        weight=1
    )


create_query_button(
    button_frame,
    "all manga",
    show_all_manga,
    0
)

create_query_button(
    button_frame,
    "currently reading",
    show_reading,
    1
)

create_query_button(
    button_frame,
    "completed",
    show_completed,
    2
)

create_query_button(
    button_frame,
    "favourites",
    show_favourites,
    3
)

create_query_button(
    button_frame,
    "rated 8.5+",
    show_high_rated,
    4
)


# results card
results_frame = tk.Frame(
    main_container,
    background=panel_colour,
    highlightbackground=border_colour,
    highlightthickness=1
)

results_frame.pack(
    fill="both",
    expand=True
)


# heading above the table
results_header = tk.Frame(
    results_frame,
    background=panel_colour
)

results_header.pack(
    fill="x",
    padx=18,
    pady=(15, 10)
)


current_query_label = tk.Label(
    results_header,
    text="all manga",
    font=("Segoe UI", 15, "bold"),
    foreground=text_colour,
    background=panel_colour
)

current_query_label.pack(
    side="left"
)


result_count_label = tk.Label(
    results_header,
    text="0 results",
    font=("Segoe UI", 9),
    foreground=orange_colour,
    background=panel_colour
)

result_count_label.pack(
    side="right"
)


# table and scrollbar container
table_frame = tk.Frame(
    results_frame,
    background=panel_colour
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=(0, 18)
)


results_table = ttk.Treeview(
    table_frame,
    style="Manga.Treeview"
)


vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=results_table.yview
)


horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=results_table.xview
)


results_table.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


results_table.grid(
    row=0,
    column=0,
    sticky="nsew"
)

vertical_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

horizontal_scrollbar.grid(
    row=1,
    column=0,
    sticky="ew"
)


table_frame.rowconfigure(
    0,
    weight=1
)

table_frame.columnconfigure(
    0,
    weight=1
)


# footer text
footer_label = tk.Label(
    main_container,
    text="python  •  sqlite  •  tkinter",
    font=("Segoe UI", 9),
    foreground=muted_text_colour,
    background=background_colour
)

footer_label.pack(
    anchor="e",
    pady=(12, 0)
)


# display all manga when the app opens
show_all_manga()


# keep the application running
window.mainloop()