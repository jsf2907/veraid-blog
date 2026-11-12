# Blog cover maker

Makes the 1280x720 cover for each post (navy panel + headline on the left, photo on the right).
Folders starting with `_` are not published by Jekyll, so nothing here appears on the site.

    python3 _tools/cover/make_cover.py --headline "Spot a|Fake Identity" \
        --subtitle "Check the photo.|Verify the person." \
        --photo photo.jpg --focus "60% 50%" --out assets/images/<slug>.jpg

- `|` forces a line break. Keep the headline to 2 to 4 words.
- Photos: free-license photos from Unsplash (license=free, no Unsplash+). No recognizable faces, logos or phone screens.
- No `--photo` = navy/blue graphic with no photo (fallback).
- Font: Inter (SIL Open Font License, see fonts/LICENSE-Inter.txt).
