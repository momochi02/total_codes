Tạo giao diện web dashboard hiện đại và chuyên nghiệp để xem kết quả chạy Fotal Update.

Dashboard gồm:

1. Thông tin request
- Request ID
- Device
- Update type
- Status
- Created by
- Latest running step

2. Hệ thống execution log
- Nút mở execution logs
- Drawer/panel bên phải
- Timeline các step
- Mỗi step có status:
  completed, running, failed, pending, skipped
- Click step để xem log chi tiết

3. Kết quả testcase
- Search testcase
- Filter theo status
- Danh sách testcase dạng card
- Hiển thị:
  before result
  after result
  compare result
  Create a professional React web app for OPIC learning and speaking practice.

Goal:
Build a clean, modern, easy-to-use OPIC practice website. The app helps users study many OPIC topics. Each topic has many questions. Each question has an audio file, question text, sample answer, and user answer input.

Tech requirements:
- Use ReactJS
- Use JavaScript, not TypeScript
- Use Vite
- No backend for now
- Use local JSON data
- Use local audio files from /public/audio
- Use CSS module or normal CSS
- Clean component structure
- Responsive desktop-first layout
- Professional UI/UX
- Export all components properly

Main features:

1. Dashboard page
Show:
- total topics
- total questions
- practiced questions
- difficult questions
- recent practice list
- continue practice button

2. Topic Library page
Show all OPIC topics as cards.
Each topic card must show:
- topic name
- short description
- number of questions
- progress, for example 5/20
- difficulty level tags: IL, IM, IH, AL
- button: Start Practice
- button: View Questions

Add search and filter:
- search topic by keyword
- filter by level
- filter by progress status

3. Question List page
When user selects a topic, show all questions in that topic.
Each question row/card must show:
- question number
- question text preview
- status: Not practiced / Practiced / Difficult
- audio available icon
- buttons: Practice, Mark Difficult

Add filter:
- All
- Not practiced
- Practiced
- Difficult

4. Practice page
This is the most important page.

Layout:
- top breadcrumb: Topic > Question X/Y
- audio player section
- question text section
- user answer textarea
- sample answer section
- navigation buttons

Required functions:
- play question audio
- replay audio
- change speed: 0.75x / 1x / 1.25x
- show/hide question text
- show/hide sample answer
- allow user to type their answer
- save answer to localStorage
- mark question as difficult
- next question
- previous question
- show progress in current topic

Practice UX:
- By default, question text is visible because beginner users need support.
- Add a toggle: “Hide question text for listening practice”.
- Sample answer must be hidden by default.
- User answer must be saved automatically to localStorage.
- If user already answered before, load saved answer.

5. Review page
Show saved answers from localStorage.
Each review item shows:
- topic name
- question text
- user answer
- sample answer
- difficult status
- last updated time

6. Data structure
Create a sample JSON file:

src/data/opicQuestions.json

Use this structure:

[
  {
    "id": "self_introduction",
    "name": "Self Introduction",
    "description": "Practice questions about introducing yourself.",
    "levels": ["IL", "IM"],
    "questions": [
      {
        "id": "self_001",
        "questionText": "Can you tell me about yourself?",
        "audioUrl": "/audio/self_introduction/self_001.mp3",
        "sampleAnswer": "Sure. My name is Anna. I work as a software tester. In my free time, I enjoy listening to music and learning English.",
        "level": "IM"
      }
    ]
  }
]

Add at least 5 sample topics:
- Self Introduction
- Home & Family
- Work
- Hobbies
- Travel

Each topic should have at least 5 sample questions.

7. Suggested folder structure:

src/
  App.jsx
  main.jsx
  data/
    opicQuestions.json
  pages/
    Dashboard.jsx
    TopicLibrary.jsx
    QuestionList.jsx
    PracticePage.jsx
    ReviewPage.jsx
  components/
    AppHeader.jsx
    Sidebar.jsx
    TopicCard.jsx
    QuestionCard.jsx
    AudioPracticePlayer.jsx
    ProgressBadge.jsx
    StatCard.jsx
  utils/
    storage.js
  styles/
    global.css

8. UI design requirements:
- Clean professional learning dashboard style
- Soft background color
- White cards
- Light border
- Rounded corners
- Good spacing
- Easy to scan
- Not too colorful
- Use one primary color
- Use clear typography
- Desktop layout with sidebar
- Mobile responsive layout
- Buttons must have hover states
- Active menu item should be highlighted

Preferred colors:
- Primary: #607D8B
- Text: #1F2937
- Muted text: #6B7280
- Border: #E5E7EB
- Background: #F8FAFC
- Card background: #FFFFFF
- Success: #16A34A
- Warning: #F59E0B
- Danger: #DC2626

9. Important UX details:
- Do not make the interface cluttered.
- Question text must be easy to read.
- Audio player must be clearly visible.
- Practice page should feel focused, not overloaded.
- Sample answer should be collapsible.
- User should always know current topic and question number.
- Progress should be visible.

10. Output:
Generate all necessary React files with clean code.
Make sure the app can run with:
npm install
npm run dev

Do not use external UI libraries.
Do not use TypeScript.
Do not create backend code.
