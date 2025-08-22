# Post-Presidency Corpus Building Guide (2021-2023)

This directory contains the infrastructure for building a comprehensive corpus of Donald Trump's post-presidency speeches and rallies from 2021-2023.

## Current Status

- ✅ **CPAC 2021**: Successfully extracted from web transcript (Rev.com)
- 🔄 **30 Events Identified**: Major rallies and speeches catalogued
- 📋 **Search Infrastructure**: YouTube search guides and batch extraction tools ready
- ❌ **74+ Speeches Missing**: Need video-to-text extraction

## Strategy: Video-to-Text Extraction

Since web transcripts are extremely limited for this period (only 1 found), we're using **video-to-text extraction** as the primary method:

1. **Identify Video Targets**: 30 major events catalogued with dates, locations, and event types
2. **Manual Video Discovery**: Use generated search guides to find YouTube videos
3. **Batch Transcript Extraction**: Process multiple videos using enhanced transcript extractor
4. **Metadata Generation**: Automatically generate spec-compliant metadata

## Files and Tools

### Generated Files
- `post_presidency_video_targets.json` - Complete event manifest (30 events)
- `post_presidency_video_targets.txt` - Human-readable event summary
- `youtube_search_urls.json` - Machine-readable search URLs
- `youtube_search_guide.html` - **Interactive HTML guide for finding videos**
- `youtube_search_guide.txt` - Text format search guide
- `video_urls_template.txt` - Template for adding found video URLs

### Extraction Tools
- `scripts/corpus_tools/enhanced_transcript_extractor.py` - Core transcript extraction
- `scripts/corpus_tools/batch_post_presidency_extractor.py` - Batch processing
- `scripts/corpus_tools/identify_post_presidency_videos.py` - Event identification
- `scripts/corpus_tools/generate_video_search_urls.py` - Search URL generation

## Workflow

### Phase 1: Video Discovery (Manual)
1. **Open the search guide**: `youtube_search_guide.html` in your browser
2. **Search for videos**: Click search links for each event
3. **Identify good candidates**: Look for videos with:
   - Relevant titles matching the event
   - Duration 10+ minutes (likely full speeches)
   - Good view counts and channel credibility
4. **Copy video URLs**: Copy URLs from promising videos

### Phase 2: URL Collection
1. **Edit the template**: Add found URLs to `video_urls_template.txt`
2. **One URL per line**: Format: `https://www.youtube.com/watch?v=VIDEO_ID`
3. **Save the file**: Ensure it's saved with `.txt` extension

### Phase 3: Batch Extraction
1. **Run batch extractor**: 
   ```bash
   python3 scripts/corpus_tools/batch_post_presidency_extractor.py
   ```
2. **Select URL file**: Choose your populated template file
3. **Confirm extraction**: Approve the batch processing
4. **Monitor progress**: Watch extraction logs and progress

### Phase 4: Review and Organize
1. **Check results**: Review extracted transcripts in `transcripts/` subdirectory
2. **Verify metadata**: Ensure JSON metadata files are generated
3. **Organize files**: Transcripts are automatically organized by event

## Event Priority

### High Priority (Start Here)
- **CPAC 2021** ✅ Already extracted
- **CPAC 2022** (2022-02-26) - Orlando, Florida
- **CPAC 2023** (2023-02-25) - National Harbor, Maryland

### Medium Priority
- **Major Rallies**: First post-presidency rallies (2021-06-26 Ohio)
- **Primary Support**: Events supporting GOP candidates
- **Election Focus**: Midterm election rallies (2022)

### Lower Priority
- **Smaller Events**: Local rallies and appearances
- **Duplicate Events**: Multiple rallies in same location

## Search Tips

### Effective Search Queries
- **Specific**: "Donald Trump CPAC 2022 Orlando Florida 2022-02-26"
- **Rally Focus**: "Donald Trump rally Ohio 2021-06-26"
- **Speech Focus**: "Donald Trump speech Arizona 2021-07-24"
- **Full Content**: "Donald Trump full speech [location] [date]"

### What to Look For
- **Duration**: 10+ minutes for full speeches, 5+ minutes for excerpts
- **Channel**: News organizations, political channels, official accounts
- **Title Relevance**: Should mention Trump, location, and event type
- **View Count**: Higher counts often indicate better quality content

### Common Sources
- **News Channels**: CNN, Fox News, MSNBC, local news
- **Political Channels**: C-SPAN, campaign channels, conservative media
- **User Uploads**: High-quality user uploads with good metadata

## Troubleshooting

### Extraction Failures
- **Check URL format**: Must be valid YouTube watch URLs
- **Verify video availability**: Some videos may be private or removed
- **Check Whisper model**: Ensure Whisper is properly installed
- **Review logs**: Check extraction logs in `logs/` subdirectory

### Quality Issues
- **Poor audio**: Try different Whisper models (base, small, medium)
- **Incomplete transcripts**: Check video duration and audio quality
- **Metadata errors**: Verify video information extraction

### Performance
- **Rate limiting**: Built-in delays prevent YouTube blocking
- **Batch size**: Process 10-20 videos at a time for best results
- **Resource usage**: Whisper models require significant memory

## Expected Outcomes

### Target Corpus Size
- **Total Events**: 30 identified
- **Target Coverage**: 20-25 transcripts (realistic expectation)
- **Quality Threshold**: High-relevance videos with good audio

### Timeline
- **Video Discovery**: 2-4 hours manual searching
- **Batch Extraction**: 1-2 hours processing time
- **Total Effort**: 3-6 hours for comprehensive coverage

## Next Steps

1. **Start with CPAC events**: High-priority, likely to have good videos
2. **Focus on major rallies**: 2021-2022 events with clear documentation
3. **Build incrementally**: Process 5-10 videos at a time
4. **Validate quality**: Review transcripts before processing more

## Support

For issues or questions:
- Check extraction logs in `logs/` subdirectory
- Review the enhanced transcript extractor documentation
- Ensure all dependencies are properly installed
- Verify YouTube video availability before extraction

---

**Note**: This approach prioritizes quality over quantity. Focus on finding high-relevance videos rather than extracting every available video. Better to have 20 high-quality transcripts than 50 poor-quality ones.
