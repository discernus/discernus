# Corpus Quality Issues - RESOLVED

## Summary
The sim2 corpus contained quality issues that have been completely resolved in sim3. All valid speeches have been copied to the clean corpus with standardized naming.

## Issues Identified and Resolved

### 1. Incomplete File (EXCLUDED)
- **File**: `30 de Setembro - Av. Paulista (2).m4a.txt`
- **Issue**: Only 14 lines vs 100+ for other speeches
- **Status**: EXCLUDED from sim3 clean corpus

### 2. Naming Inconsistencies (FIXED)
- **Issue**: Mix of Portuguese/English formats and file extensions
- **Solution**: Standardized to `speech_XX_location.txt` format

### 3. Quality Variations (DOCUMENTED)
- **Standard**: Minimum 50+ lines, complete transcripts
- **Verification**: All included files meet quality threshold

## Complete Clean Corpus (8 Valid Speeches)

| File | Lines | Size | Content |
|------|-------|------|---------|
| speech_01_aracatuba.txt | 65 | 8.0KB | Araçatuba campaign speech |
| speech_02_porto_velho.txt | 356 | 25KB | Porto Velho campaign speech |
| speech_03_juiz_de_fora.txt | 323 | 18KB | Juiz de Fora business association speech |
| speech_04_apos_atentado.txt | 788 | 23KB | After assassination attempt (16 Sept) |
| speech_05_dia_antes_eleicoes.txt | 116 | 25KB | One day before elections (6 Oct) |
| speech_06_first_round_victory.txt | 125 | 25KB | After first round victory (16 Oct) |
| speech_07_ultima_live_2o_turno.txt | 212 | 27KB | Final live before second round (27 Oct) |
| speech_08_paulista_avenue.txt | 272 | 9.1KB | Paulista Avenue rally (22 Oct) |

**Total**: 8 complete, verified speeches ranging from 65-788 lines each

## Quality Assurance
- ✅ All files have complete transcriptions
- ✅ All files meet minimum length requirements (50+ lines)
- ✅ Standardized naming convention applied
- ✅ No contamination with Eduardo validation scores
- ✅ Ready for blind coordinate-free analysis

## Corpus Usage
This clean corpus provides substantial material for coordinate-free discourse analysis across multiple campaign contexts:
- Campaign rallies (3 speeches)
- Electoral milestone speeches (3 speeches) 
- Crisis response (1 speech)
- Business outreach (1 speech)

The diverse temporal and contextual spread enables robust framework validation without methodological contamination. 