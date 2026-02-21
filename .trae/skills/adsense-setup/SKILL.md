---
name: "adsense-setup"
description: "Sets up Google AdSense for websites with required policy pages. Invoke when user wants to add Google AdSense advertising to their website."
---

# Google AdSense Setup

This skill helps set up Google AdSense for websites, including creating required policy pages.

## Google AdSense Requirements

Google AdSense requires the following pages:
1. **About Us** - Information about the website/company
2. **Privacy Policy** - How you handle user data
3. **Terms of Use** - Rules for using the website

## Required Page Content

### About Us Page (about.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>About Us - Your Site Name</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/about.html">About</a>
            <a href="/privacy.html">Privacy</a>
            <a href="/terms.html">Terms</a>
        </nav>
    </header>
    <main>
        <h1>About Us</h1>
        <p>Description of your website and mission</p>
        <h2>Contact</h2>
        <p>Email: your@email.com</p>
    </main>
    <footer>
        <p>&copy; 2026 Your Name. All rights reserved.</p>
    </footer>
</body>
</html>
```

### Privacy Policy (privacy.html)

Must include:
- Information collected
- How information is used
- Data security measures
- Third-party services (AdSense, analytics)
- Cookie policy
- Contact information

### Terms of Use (terms.html)

Must include:
- Service description
- User responsibilities
- Intellectual property
- Limitation of liability
- Disclaimer of warranties
- Termination clause
- Contact information

## AdSense Code Integration

Add to HTML `<head>`:
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_PUBLISHER_ID" crossorigin="anonymous"></script>
```

Add ad unit to page:
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-YOUR_PUBLISHER_ID"
     data-ad-slot="YOUR_AD_SLOT"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

## Required Information from User

To create these pages, ask for:
1. Website name
2. Contact email
3. Website URL
4. Developer/Company name

## Best Practices

1. Use consistent header/footer navigation across all pages
2. Include links to all policy pages in footer
3. Keep content accurate and up-to-date
4. Add Google AdSense in header for faster loading

## Usage

Invoke this skill when user wants to:
- Add Google AdSense to website
- Create Privacy Policy
- Create Terms of Use
- Create About Us page
- Prepare website for AdSense approval
