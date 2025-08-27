# Project Management Structure

This directory contains the project management files for Discernus, organized to support efficient backlog management and Cursor agent workflows.

## File Structure

### `inbox.md`
- **Purpose**: Raw capture of backlog items without organization
- **Usage**: "inbox this" → append new items here with minimal formatting
- **Content**: Simple, unformatted captures that will be groomed later

### `sprints.md`
- **Purpose**: Organized backlog with sprint planning, dependencies, and detailed specifications
- **Usage**: "groom our sprints" → organize inbox items into proper sprint structure
- **Content**: Full backlog items with sprint assignments, dependencies, and acceptance criteria

### `done.md`
- **Purpose**: Archive of completed backlog items for reference and historical tracking
- **Usage**: "log it to done" → move completed items here from sprints.md
- **Content**: Completed items with completion dates and final status

## Workflow Commands

### Quick Capture
```
"inbox this: we need to fix the RAG index persistence issue"
```
- Agent **TRULY APPENDS** to `inbox.md` with minimal formatting
- **CRITICAL**: Agent should NOT read entire file content - use append operations only
- No sprint thinking required
- Fast capture during implementation work

### Backlog Grooming
```
"groom our sprints"
```
- Agent moves all items from `inbox.md` to `sprints.md`
- Organizes items into appropriate sprints
- Maps dependencies and assigns priorities
- Clears `inbox.md` after successful grooming

### Completion Tracking
```
"log it to done"
```
- Agent moves completed items from `sprints.md` to `done.md`
- Maintains completion history
- Updates status and completion dates

## Benefits

1. **Context Efficiency**: Quick capture doesn't require parsing full backlog
2. **Focused Work**: Separate capture vs. organization activities
3. **Cursor Agent Friendly**: Clear, simple commands that agents can follow
4. **Maintainable**: Logical separation of concerns
5. **Historical Tracking**: Complete record of project progress

## Migration Notes

- Current backlog content has been migrated to `sprints.md`
- `inbox.md` is ready for new quick captures
- `done.md` is ready for completed items
- Existing `todo/` directory structure preserved for reference
