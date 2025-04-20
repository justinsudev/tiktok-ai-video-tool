from flask import Blueprint, render_template, request, current_app
import requests
import threading

bp = Blueprint("search", __name__, template_folder="../templates")

@bp.route("/", methods=["GET"])
def index():
    """Search GUI: handles query input, merges Index results, displays docs."""
    # Extract query and weight
    q = request.args.get("q", "")
    try:
        w = float(request.args.get("w", 0.5))
    except ValueError:
        w = 0.5

    results = []
    if q:
        # Concurrently fetch hits from all Index servers
        responses = []
        def fetch(url):
            r = requests.get(url, params={"q": q, "w": w})
            if r.ok:
                responses.append(r.json().get("hits", []))

        threads = [threading.Thread(target=fetch, args=(u,))
                   for u in current_app.config["SEARCH_INDEX_SEGMENT_API_URLS"]]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Combine and sort all segment hits by score descending
        all_hits = []
        for seg_hits in responses:
            all_hits.extend(seg_hits)
        all_hits_sorted = sorted(all_hits, key=lambda h: h["score"], reverse=True)
        top_hits = all_hits_sorted[:10]

        # Enrich with metadata
        from search.model import get_doc
        results = [
            {"docid": h["docid"], "score": h["score"], **get_doc(h["docid"])}
            for h in top_hits
        ]

    # Render the Jinja template
    return render_template(
        "main.html",
        results=results,
        q=q,
        w=w
    )
