from flask import Flask, render_template, request
import math

app = Flask(__name__)


def check(curr_lec, tot_lec):
    if tot_lec <= 0:
        raise ValueError("Total lectures must be greater than zero.")

    if curr_lec < 0:
        raise ValueError("Attended lectures cannot be negative.")

    if curr_lec > tot_lec:
        raise ValueError("Attended lectures cannot exceed total lectures.")

    perc = round((curr_lec / tot_lec) * 100, 2)

    # Additional consecutive lectures needed to reach 75%.
    temp = max(0, math.ceil(3 * tot_lec - 4 * curr_lec))

    val1 = curr_lec + temp
    val2 = tot_lec + temp

    return temp, val1, val2, perc


@app.route("/", methods=["GET"])
def home():
    name = request.args.get("name", "").strip()
    curr_input = request.args.get("curr_lec", "").strip()
    tot_input = request.args.get("tot_lec", "").strip()

    # Default dashboard.
    if not name and not curr_input and not tot_input:
        return render_template(
            "index.html",
            name="",
            temp=None,
            val1=None,
            val2=None,
            per=None,
            error=None
        )

    # Initialize results before validation.
    temp = val1 = val2 = perc = None

    try:
        if not name:
            raise ValueError("Please enter your name.")

        if not curr_input or not tot_input:
            raise ValueError("Please enter both lecture counts.")

        curr_lec = int(curr_input)
        tot_lec = int(tot_input)

        if not 0 <= curr_lec <= 200:
            raise ValueError("Attended lectures must be between 0 and 200.")

        if not 1 <= tot_lec <= 200:
            raise ValueError("Total lectures must be between 1 and 200.")

        temp, val1, val2, perc = check(curr_lec, tot_lec)

        error = None

    except ValueError as e:
        error = str(e)

    return render_template(
        "index.html",
        name=name,
        temp=temp,
        val1=val1,
        val2=val2,
        per=perc,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)