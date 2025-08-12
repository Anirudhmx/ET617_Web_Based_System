# 🚀 Free Hosting Deployment Guide

## Option 1: Render (Recommended - Easiest)

### Step 1: Prepare Your Repository
1. Push your code to GitHub
2. Make sure you have these files:
   - `main.py` ✅
   - `requirements.txt` ✅ (Updated with compatible versions)
   - `Procfile` ✅
   - `runtime.txt` ✅ (Updated to Python 3.11.9)
   - `build.sh` ✅ (New build script)

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `et617-learning-platform`
   - **Environment**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn main:app`
5. Click "Create Web Service"

### Step 3: Set Environment Variables
In Render dashboard, go to Environment → Add:
- `SECRET_KEY`: Generate a random string (e.g., `your-super-secret-key-123`)
- `DATABASE_URL`: Leave empty for SQLite (or use PostgreSQL for production)

### Step 4: Deploy
- Render will automatically build and deploy your app
- Your site will be available at: `https://your-app-name.onrender.com`

---

## 🔧 Troubleshooting Build Errors

### If you get "Getting requirements to build wheel" errors:

1. **Use the updated `requirements.txt`** (already done)
2. **Use Python 3.11.9** (already done)
3. **Use the custom build script** (already done)

### Alternative Build Command (if build.sh fails):
```
pip install --upgrade pip && pip install --upgrade wheel setuptools && pip install -r requirements.txt
```

### If you still get errors, try this minimal requirements.txt:
```
Flask==2.2.5
Flask-SQLAlchemy==3.0.3
Flask-Login==0.6.2
Werkzeug==2.2.3
gunicorn==20.1.0
```

---

## Option 2: Railway (Alternative)

### Step 1: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy

### Step 2: Configure
- Add environment variables in Railway dashboard
- Railway provides a PostgreSQL database automatically

---

## Option 3: PythonAnywhere

### Step 1: Setup
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create free account
3. Go to "Web" tab → "Add a new web app"

### Step 2: Configure
1. Choose "Flask" framework
2. Set Python version to 3.11
3. Upload your files via Files tab
4. Install requirements: `pip install -r requirements.txt`

---

## ⚠️ Important Notes

### Database Considerations
- **SQLite**: Works locally but not recommended for production
- **PostgreSQL**: Better for production (Render/Railway provide this)

### File Uploads
- Your `uploads/` folder won't persist on free tiers
- Consider using cloud storage (AWS S3, Cloudinary) for production

### Environment Variables
Always set these in production:
- `SECRET_KEY`: Random string for security
- `DATABASE_URL`: Database connection string

### Performance
- Free tiers have limitations
- App may sleep after inactivity (Render)
- Limited bandwidth and storage

---

## 🎯 Quick Start with Render

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix deployment configuration"
   git push origin main
   ```

2. **Deploy on Render**:
   - Follow Step 2 above
   - Use build command: `chmod +x build.sh && ./build.sh`
   - Wait for build (5-10 minutes)
   - Your app will be live!

3. **Custom Domain** (Optional):
   - In Render dashboard → Settings → Custom Domains
   - Add your domain and configure DNS

---

## 🔧 Troubleshooting

### Common Issues:
- **Build fails**: Use the updated requirements.txt and build.sh
- **App crashes**: Check logs in hosting dashboard
- **Database errors**: Ensure database is properly configured
- **Static files not loading**: Check file paths and permissions

### Debug Mode:
- Set `debug=False` in production
- Check hosting platform logs for errors

---

## 📱 Your App Features
Your learning platform includes:
- ✅ User authentication (login/register)
- ✅ Course management
- ✅ Video lectures and text lessons
- ✅ Clickstream analytics
- ✅ Data export functionality
- ✅ Responsive design

Perfect for educational purposes and learning analytics!
