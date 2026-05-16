# RetrofitList.ie

Ireland's home retrofit directory and news hub. A static website connecting homeowners with trusted retrofit professionals, and keeping them informed on grants, guides, and regulations.

---

## How to Add a New Provider

Open `data/providers.json` in any text editor. Add a new entry to the end of the JSON array, following this exact format:

```json
{
  "id": 15,
  "name": "Your Company Name",
  "county": "Cork",
  "categories": ["Heat Pumps"],
  "phone": "021 123 4567",
  "email": "info@yourcompany.ie",
  "website": "https://yourcompany.ie",
  "description": "A 2–4 sentence description of your business, the services you offer, the areas you cover, and any relevant accreditations.",
  "featured": false
}
```

**Field notes:**

| Field | Required | Notes |
|---|---|---|
| `id` | Yes | Must be unique. Use the next number in sequence. |
| `name` | Yes | The company's trading name. |
| `county` | Yes | Must match an Irish county name exactly, e.g. `"Dublin"`, `"Cork"`, `"Galway"`. |
| `categories` | Yes | An array. A provider can have more than one. Must be chosen from the list below. |
| `phone` | Yes | Irish format, e.g. `"01 234 5678"`. |
| `email` | Yes | Contact email address. |
| `website` | No | Full URL including `https://`. Leave as `""` if none. |
| `description` | Yes | Plain text, 2–4 sentences. No HTML. |
| `featured` | No | Set to `true` to show this provider in the Featured section on the homepage. Only 3 featured providers are shown; set the rest to `false`. |

**Valid category values** (copy exactly, including capitalisation and punctuation):

- `"BER Assessors"`
- `"External Wall Insulation"`
- `"Internal Wall Insulation"`
- `"Attic & Floor Insulation"`
- `"Heat Pumps"`
- `"Solar PV"`
- `"Airtightness Testing"`
- `"MVHR / Ventilation"`
- `"Windows & Doors"`
- `"One-Stop-Shop Retrofit Contractors"`

Make sure the file remains valid JSON when you save it — every entry except the last must end with a comma `,`. You can paste the contents into [jsonlint.com](https://jsonlint.com) to check for errors.

---

## How to Add a New Article

Open `data/articles.json` in any text editor. Add a new entry to the end of the JSON array:

```json
{
  "id": 7,
  "title": "Your Article Title",
  "date": "2025-06-01",
  "category": "SEAI Grants",
  "author": "Your Name",
  "summary": "A one or two sentence summary shown on article cards and listing pages.",
  "body": [
    "First paragraph of the article. Write as much as you like here.",
    "Second paragraph. Each item in this array becomes a separate paragraph.",
    "Third paragraph, and so on."
  ]
}
```

**Field notes:**

| Field | Required | Notes |
|---|---|---|
| `id` | Yes | Must be unique. Use the next number in sequence. |
| `title` | Yes | The article headline. |
| `date` | Yes | Format: `"YYYY-MM-DD"`, e.g. `"2025-06-15"`. |
| `category` | Yes | Must be one of the five valid categories listed below. |
| `author` | Yes | Author's name, e.g. `"Jane Smith"` or `"RetrofitList Editorial Team"`. |
| `summary` | Yes | Short summary shown on article cards. 1–2 sentences. |
| `body` | Yes | An array of strings. Each string is one paragraph. No HTML needed. |

**Valid category values:**

- `"SEAI Grants"`
- `"Local Authority Grants"`
- `"How-To Guides"`
- `"Planning & Regulations"`
- `"Market News"`

Articles are automatically sorted by date (newest first) on the News page, so you don't need to worry about order in the file.

---

## Running the Site Locally

Because the site loads data using `fetch()`, you must serve it from a local web server — browsers block fetch requests from `file://` URLs for security reasons.

The easiest options:

**VS Code Live Server** (recommended)
1. Install the [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) in VS Code.
2. Open the project folder in VS Code.
3. Click **Go Live** in the bottom status bar.
4. The site opens at `http://127.0.0.1:5500`.

**Python (if installed)**
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

---

## Deploying to GitHub Pages

1. Push this repository to GitHub (you've already done this at `github.com/strongwords101/retrofit-ireland`).
2. Go to **Settings → Pages** in your repository.
3. Under **Source**, select **Deploy from a branch**, choose `main`, folder `/` (root), and click **Save**.
4. After a minute or two, your site will be live at `https://strongwords101.github.io/retrofit-ireland/`.

The site works on GitHub Pages without any build steps — just push changes to `main` and they go live automatically.

---

## File Structure

```
retrofit-ireland/
├── index.html          Homepage
├── directory.html      Provider directory with filters
├── news.html           News & guides listing
├── about.html          About page and listing request info
├── article.html        Individual article view (loaded from URL ?id=)
├── css/
│   └── styles.css      All styles
├── js/
│   └── main.js         All JavaScript (data loading, rendering, filters)
└── data/
    ├── providers.json  All provider listings — edit this to add providers
    └── articles.json   All articles — edit this to add articles
```

No build tools, no npm, no frameworks. Edit the JSON files and push — that's it.
