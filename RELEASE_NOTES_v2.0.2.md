# Release Notes v2.0.2

## 📅 Release Date
2026-02-04

## 🎉 Release Summary

Version 2.0.2 is a feature release that improves the duplicate handling by preserving queue positions through email correction instead of deletion.

## ✨ Key Feature: Warteplatz-Erhaltung (Queue Position Preservation)

### The Problem (V2.0.1)
- Person registers at 10:00 with typo email (ID 10)
- Person registers at 10:30 with correct email (ID 42)
- V2.0.1: ID 42 kept, ID 10 deleted
- **→ Queue position from 10:00 was lost!** ❌

### The Solution (V2.0.2)
- ID 10: Email is **automatically corrected** (typo → correct)
- ID 42: Removed as duplicate (later registration)
- **→ Queue position from 10:00 is preserved!** ✅

## 🆕 New Features

### 1. Email Correction Logic
- Detects best email for each person (highest quality score)
- Automatically corrects typo emails to best email
- Removes duplicates after email correction
- Creates correction report: `*_email_korrekturen.csv`

### 2. GUI Option
- New checkbox: **"📧 Email-Typos automatisch korrigieren"**
- Default: **ON** (recommended)
- Can be disabled to revert to V2.0.1 behavior

### 3. New Output File
**`*_email_korrekturen.csv`** - List of all corrected emails:
- Columns: ID, Name, Old Email, New Email, Reason
- Only created when corrections were made

## 📊 Impact

| Scenario | V2.0.1 | V2.0.2 |
|----------|--------|--------|
| Early registration with typo email | ❌ Deleted | ✅ Email corrected |
| Late registration with correct email | ✅ Kept | ❌ Deleted (duplicate) |
| Queue position | ❌ Lost | ✅ Preserved |

## ✅ Testing Status

**User Confirmation:** "bin zufriden, alles scheint zu funktionieren"
- Duplicate detection working correctly
- Email correction (Pflücke/Pluecke fix) confirmed working
- All output files generated correctly

## 📦 Deliverables

### Executables
Built automatically via GitHub Actions for:
- Windows: `Mediball_Duplikat_Filter_Windows.exe`
- Mac: `Mediball_Duplikat_Filter_Mac`
- Linux: `Mediball_Duplikat_Filter_Linux`

### Documentation
- ✅ README.md updated with:
  - Version 2.0.2
  - Installation instructions (executables + Python)
  - Usage guide with step-by-step instructions
  - CSV format requirements
  - Output files description
- ✅ CHANGELOG.md updated with detailed v2.0.2 entry
- ✅ VERSION file set to 2.0.2
- ✅ Code version set to 2.0.2

### Code Quality
- ✅ No TODO or FIXME items
- ✅ No debug statements
- ✅ Python syntax validated
- ✅ Dependencies up to date (pandas>=2.0.0)
- ✅ CodeQL security scan passed
- ✅ All code properly formatted

## 🚀 Release Process

### Steps to Complete Release

1. **Merge PR** to main branch
2. **Create Tag** on main branch:
   ```bash
   git checkout main
   git pull origin main
   git tag -a v2.0.2 -m "Release version 2.0.2"
   git push origin v2.0.2
   ```
3. **GitHub Actions** will automatically:
   - Build executables for all platforms
   - Create GitHub Release
   - Attach executables to release

### Verification

After tag is pushed:
1. Check GitHub Actions: https://github.com/Fi-schi/mediball-duplicate-filter/actions
2. Verify Release created: https://github.com/Fi-schi/mediball-duplicate-filter/releases
3. Test downloads for each platform

## 📝 Upgrade Recommendation

**All users should upgrade to v2.0.2** for:
- Better queue position preservation
- Improved email handling
- More transparent reporting

## 🔄 Version History

- **v2.0.2** (2026-02-04) - Email correction for queue position preservation
- **v2.0.1** (2026-02-04) - Bugfix: Email-name typo detection
- **v2.0.0** (2026-02-04) - Production polish release
- **v1.7.8** (2026-02-03) - Hybrid domain intelligence
- **v1.7.7** (2026-02-03) - Domain typo correction

## 📞 Support

For issues or questions:
- Check existing issues: https://github.com/Fi-schi/mediball-duplicate-filter/issues
- Create new issue with detailed description

---

**Release prepared by:** GitHub Copilot
**Release approval:** Pending merge to main branch
