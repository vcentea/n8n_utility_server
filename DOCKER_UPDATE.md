# Docker Update & Deployment Guide

This guide covers updating your Docker deployment with the latest code from git.

## Update Scripts

Two scripts are provided for updating your Docker deployment:

- **Linux/Mac:** `update_docker.sh`
- **Windows:** `update_docker.bat`

Both scripts perform the same operations:
1. Back up your current `.env` file
2. Pull the latest code from git
3. Restore your API key and configuration
4. Rebuild Docker containers
5. Restart the service

## Usage

### First-Time Deployment

```bash
# Linux/Mac
./update_docker.sh

# Windows
update_docker.bat
```

If `.env` doesn't exist, the script will:
1. Create `.env` from `.env.example`
2. Prompt you to set your `API_KEY`
3. Exit so you can configure it

After setting your API_KEY, run the script again.

### Updating Existing Deployment

Simply run the script:

```bash
# Linux/Mac
./update_docker.sh

# Windows
update_docker.bat
```

The script will:
- ✅ Preserve your API_KEY and settings
- ✅ Pull latest code changes
- ✅ Rebuild containers with new code
- ✅ Restart the service automatically

## What Gets Updated

- Application code
- Dependencies (requirements.txt)
- Docker configuration
- API endpoints and features

## What Stays the Same

- Your `.env` configuration (backed up to `.env.backup`)
- Your API_KEY
- Port settings
- Volume data

## Manual Docker Commands

If you prefer manual control:

```bash
# Stop containers
docker-compose down

# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker-compose logs
```

### API Key Issues

1. Check `.env` file exists
2. Verify `API_KEY` is set
3. If needed, restore from `.env.backup`

### Git Conflicts

If you have local changes:
```bash
# View your changes
git status

# Stash changes (saved automatically by update script)
git stash list

# Restore your changes if needed
git stash pop
```

### Port Already in Use

Edit `.env` and change the PORT:
```bash
PORT=3377
```

Then rebuild:
```bash
docker-compose down
docker-compose up -d
```

## Rollback

If an update causes issues:

```bash
# Stop containers
docker-compose down

# Restore previous code
git log --oneline  # Find the previous commit
git checkout <previous-commit-hash>

# Restore previous .env if needed
cp .env.backup .env

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d
```

## Scheduled Updates

You can automate updates using cron (Linux) or Task Scheduler (Windows):

### Linux Cron Example

```bash
# Edit crontab
crontab -e

# Add line to update daily at 2 AM
0 2 * * * cd /path/to/n8n_utility_server && ./update_docker.sh >> update.log 2>&1
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 2 AM)
4. Action: Start a program
5. Program: `E:\path\to\update_docker.bat`
6. Start in: `E:\path\to\n8n_utility_server`

## Monitoring

After update, verify the service:

```bash
# Check if running
docker-compose ps

# Test the endpoint
curl http://localhost:2277/health

# View recent logs
docker-compose logs --tail=50
```

## Backup Strategy

The update script automatically backs up `.env`, but consider:

1. **Regular backups** of your `.env` file
2. **Document** your configuration changes
3. **Test** updates in a staging environment first

## Security Notes

- Keep your API_KEY secure
- Don't commit `.env` to git
- Regularly update to get security patches
- Use strong API keys (generated, not default)

## Support

- **Documentation:** See README.md, API_USAGE.md
- **Issues:** Check container logs first
- **Manual deployment:** See DEPLOYMENT.md


