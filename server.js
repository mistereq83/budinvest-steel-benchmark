const express = require('express');
const path = require('path');
const compression = require('compression');
const { Resend } = require('resend');

const app = express();
const PORT = process.env.PORT || 3000;

// Gzip compression
app.use(compression());

// JSON parsing
app.use(express.json());

// Security headers
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    next();
});

// Resend configuration
const resend = new Resend('REDACTED_RESEND_KEY');

// Turnstile verification
async function verifyTurnstile(token) {
    const secret = 'REDACTED_TURNSTILE_SECRET';
    
    try {
        const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                secret: secret,
                response: token,
            }),
        });

        const result = await response.json();
        return result.success;
    } catch (error) {
        console.error('Turnstile verification error:', error);
        return false;
    }
}

// Contact form endpoint
app.post('/api/contact', async (req, res) => {
    try {
        const { name, company, email, phone, subject, message, 'cf-turnstile-response': turnstileToken } = req.body;

        // Validate required fields
        if (!name || !email || !subject || !message) {
            return res.status(400).json({ error: 'Uzupełnij wszystkie wymagane pola' });
        }

        if (!turnstileToken) {
            return res.status(400).json({ error: 'Weryfikacja antyspamowa jest wymagana' });
        }

        // Verify Turnstile
        const isValidTurnstile = await verifyTurnstile(turnstileToken);
        if (!isValidTurnstile) {
            return res.status(400).json({ error: 'Weryfikacja antyspamowa nie powiodła się' });
        }

        // Prepare email content
        const subjectMap = {
            'wycena-konstrukcje': 'Wycena — konstrukcje stalowe',
            'wycena-zbiorniki': 'Wycena — zbiorniki ciśnieniowe', 
            'wycena-rurociagi': 'Wycena — rurociągi przemysłowe',
            'wycena-obrobka': 'Wycena — obróbka metali',
            'wycena-beton': 'Wycena — prefabrykacja betonu',
            'rekrutacja': 'Rekrutacja / Praca',
            'inne': 'Inne'
        };

        const emailSubject = `[Budinvest Steel] ${subjectMap[subject] || subject}`;
        
        const emailHtml = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
                .header { background: #1a365d; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9f9f9; }
                .field { margin-bottom: 15px; padding: 10px; background: white; border-left: 4px solid #3182ce; }
                .field-label { font-weight: bold; color: #1a365d; }
                .field-value { margin-top: 5px; }
                .footer { background: #e2e8f0; padding: 15px; text-align: center; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Nowe zapytanie z formularza kontaktowego</h2>
                <p>Budinvest Steel</p>
            </div>
            
            <div class="content">
                <div class="field">
                    <div class="field-label">Imię i nazwisko:</div>
                    <div class="field-value">${name}</div>
                </div>
                
                ${company ? `
                <div class="field">
                    <div class="field-label">Firma:</div>
                    <div class="field-value">${company}</div>
                </div>
                ` : ''}
                
                <div class="field">
                    <div class="field-label">Email:</div>
                    <div class="field-value">${email}</div>
                </div>
                
                ${phone ? `
                <div class="field">
                    <div class="field-label">Telefon:</div>
                    <div class="field-value">${phone}</div>
                </div>
                ` : ''}
                
                <div class="field">
                    <div class="field-label">Temat zapytania:</div>
                    <div class="field-value">${subjectMap[subject] || subject}</div>
                </div>
                
                <div class="field">
                    <div class="field-label">Wiadomość:</div>
                    <div class="field-value">${message.replace(/\n/g, '<br>')}</div>
                </div>
            </div>
            
            <div class="footer">
                <p>Wiadomość została wysłana automatycznie z formularza kontaktowego na stronie budinvest-steel.com</p>
                <p>Data: ${new Date().toLocaleString('pl-PL')}</p>
            </div>
        </body>
        </html>
        `;

        // Send email via Resend
        const data = await resend.emails.send({
            from: 'noreply@budinvest-steel.com',
            to: 'kontakt@bud-invest.com',
            replyTo: email,
            subject: emailSubject,
            html: emailHtml,
        });

        console.log('Email sent successfully:', data.id);
        res.json({ success: true });

    } catch (error) {
        console.error('Contact form error:', error);
        res.status(500).json({ error: 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.' });
    }
});

// Static files with cache
app.use(express.static(path.join(__dirname, 'public'), {
    maxAge: '7d',
    etag: true
}));

// English routes
app.get('/en/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'en', 'index.html'), err => { if (err) res.status(404).send('Page not found'); });
});
app.get('/en/about', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'en', 'about.html'), err => { if (err) res.status(404).send('Page not found'); });
});
app.get('/en/services', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'en', 'services.html'), err => { if (err) res.status(404).send('Page not found'); });
});
app.get('/en/services/:page', (req, res) => {
    const pageMap = {
        'steel-structures': 'steel-structures',
        'pressure-vessels': 'pressure-vessels',
        'industrial-pipelines': 'industrial-pipelines',
        'metal-processing': 'metal-processing',
        'concrete-prefabrication': 'concrete-prefabrication'
    };
    const page = pageMap[req.params.page];
    if (page) {
        res.sendFile(path.join(__dirname, 'public', 'en', 'services', `${page}.html`), err => { if (err) res.status(404).send('Page not found'); });
    } else {
        res.status(404).send('Page not found');
    }
});
app.get('/en/:page', (req, res) => {
    const pageMap = {
        'projects': 'projects',
        'certifications': 'certifications',
        'machinery': 'machinery',
        'careers': 'careers',
        'contact': 'contact'
    };
    const page = pageMap[req.params.page];
    if (page) {
        res.sendFile(path.join(__dirname, 'public', 'en', `${page}.html`), err => { if (err) res.status(404).send('Page not found'); });
    } else {
        res.status(404).send('Page not found');
    }
});

// German routes
app.get('/de/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'de', 'index.html'), err => { if (err) res.status(404).send('Page not found'); });
});
app.get('/de/ueber-uns', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'de', 'ueber-uns.html'), err => { if (err) res.status(404).send('Page not found'); });
});
app.get('/de/leistungen', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'de', 'leistungen.html'), err => { if (err) res.status(404).send('Page not found'); });
});
app.get('/de/leistungen/:page', (req, res) => {
    const pageMap = {
        'stahlkonstruktionen': 'stahlkonstruktionen',
        'druckbehaelter': 'druckbehaelter',
        'industrierohrleitungen': 'industrierohrleitungen',
        'metallbearbeitung': 'metallbearbeitung',
        'betonfertigteile': 'betonfertigteile'
    };
    const page = pageMap[req.params.page];
    if (page) {
        res.sendFile(path.join(__dirname, 'public', 'de', 'leistungen', `${page}.html`), err => { if (err) res.status(404).send('Page not found'); });
    } else {
        res.status(404).send('Page not found');
    }
});
app.get('/de/:page', (req, res) => {
    const pageMap = {
        'projekte': 'projekte',
        'zertifikate': 'zertifikate',
        'maschinenpark': 'maschinenpark',
        'karriere': 'karriere',
        'kontakt': 'kontakt'
    };
    const page = pageMap[req.params.page];
    if (page) {
        res.sendFile(path.join(__dirname, 'public', 'de', `${page}.html`), err => { if (err) res.status(404).send('Page not found'); });
    } else {
        res.status(404).send('Page not found');
    }
});

// Privacy policy routes
app.get('/polityka-prywatnosci', (req, res) => res.sendFile(path.join(__dirname, 'public', 'polityka-prywatnosci.html')));
app.get('/en/privacy-policy', (req, res) => res.sendFile(path.join(__dirname, 'public', 'en', 'privacy-policy.html')));
app.get('/de/datenschutz', (req, res) => res.sendFile(path.join(__dirname, 'public', 'de', 'datenschutz.html')));

// Polish routes (existing)
app.get('/:page', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'public', `${req.params.page}.html`), err => { if (err) next(); });
});
app.get('/uslugi/:page', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'public', 'uslugi', `${req.params.page}.html`), err => { if (err) next(); });
});
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.use((req, res) => {
    res.status(404).sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => console.log(`Budinvest Steel running on port ${PORT}`));
