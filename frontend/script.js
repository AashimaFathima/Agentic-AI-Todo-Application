const API_URL = "http://127.0.0.1:8000";


// ============================================================
// DATE
// ============================================================

const today = new Date();

document.getElementById("todayDate").textContent =
    today.toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric"
    });


// ============================================================
// CHAT
// ============================================================

const chatInput = document.getElementById("chatInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");


function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className =
        sender === "user"
            ? "message user-message"
            : "message assistant-message";


    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent =
        sender === "user"
            ? "You"
            : "✦";


    const content = document.createElement("div");

    content.className = "message-content";


    const name = document.createElement("span");

    name.className = "message-name";

    name.textContent =
        sender === "user"
            ? "You"
            : "Luma";


    const bubble = document.createElement("div");

    bubble.className = "message-bubble";

    bubble.innerHTML = marked.parse(text);


    content.appendChild(name);
    content.appendChild(bubble);

    message.appendChild(avatar);
    message.appendChild(content);

    chatMessages.appendChild(message);


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


async function sendMessage() {

    const message = chatInput.value.trim();

    if (!message) {
        return;
    }


    addMessage(message, "user");

    chatInput.value = "";

    sendButton.disabled = true;


    try {

        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data = await response.json();


        addMessage(
            data.response,
            "assistant"
        );


        // Refresh dashboard after the Agent changes tasks
        await loadTasks();

        // Refresh Google Calendar after the Agent
        // creates, updates, or deletes a calendar event
        if (googleCalendar) {
            googleCalendar.refetchEvents();
        }

    }

    catch (error) {

        console.error(error);

        addMessage(
            "I couldn't connect to the backend. Make sure FastAPI is running.",
            "assistant"
        );
    }

    finally {

        sendButton.disabled = false;

        chatInput.focus();
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


chatInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


function usePrompt(prompt) {

    chatInput.value = prompt;

    chatInput.focus();
}


// ============================================================
// TASK DATA
// ============================================================

let allTasks = [];


// ============================================================
// TASKS
// ============================================================

async function loadTasks() {

    try {

        const response = await fetch(
            `${API_URL}/tasks`
        );


        if (!response.ok) {

            throw new Error(
                `Failed to load tasks: ${response.status}`
            );
        }


        const tasks = await response.json();


        // Store tasks globally
        allTasks = tasks;


        // ================= STATS =================

        const pendingCount =
            tasks.filter(task => !task.completed).length;


        const completedCount =
            tasks.filter(task => task.completed).length;


        // Use local date instead of UTC
        const currentDate =
            new Date();


        const todayString =
            `${currentDate.getFullYear()}-${String(
                currentDate.getMonth() + 1
            ).padStart(2, "0")}-${String(
                currentDate.getDate()
            ).padStart(2, "0")}`;


        const todayCount =
            tasks.filter(task =>
                task.due_date &&
                task.due_date.startsWith(todayString)
            ).length;


        document.querySelector(
            ".stat-card.peach strong"
        ).textContent = pendingCount;


        document.querySelector(
            ".stat-card.violet strong"
        ).textContent = todayCount;


        document.querySelector(
            ".stat-card.white strong"
        ).textContent = completedCount;


        // ================= TASK LIST =================

        const taskList =
            document.querySelector(".task-list");


        const taskCount =
            document.querySelector(".task-count");


        taskList.innerHTML = "";


        taskCount.textContent =
            `${tasks.length} tasks`;


        tasks.forEach(task => {

            const taskItem =
                document.createElement("div");

            taskItem.className =
                "task-item";


            const checkbox =
                document.createElement("div");

            checkbox.className =
                "task-checkbox";


            if (task.completed) {

                checkbox.classList.add(
                    "completed"
                );

                checkbox.textContent = "✓";
            }


            const taskInfo =
                document.createElement("div");

            taskInfo.className =
                "task-info";


            const title =
                document.createElement("strong");

            title.textContent =
                task.title;


            const description =
                document.createElement("span");

            description.textContent =
                task.description;


            taskInfo.appendChild(title);

            taskInfo.appendChild(description);


            taskItem.appendChild(checkbox);

            taskItem.appendChild(taskInfo);


            taskList.appendChild(taskItem);
        });

    }

    catch (error) {

        console.error(
            "Could not load tasks:",
            error
        );
    }
}


// ============================================================
// GOOGLE CALENDAR
// ============================================================

let googleCalendar;


function initializeCalendar() {

    const calendarElement =
        document.getElementById("calendar");


    googleCalendar =
        new FullCalendar.Calendar(
            calendarElement,
            {

                initialView: "dayGridMonth",

                timeZone: "Asia/Kolkata",

                height: "auto",

                firstDay: 0,

                dayMaxEvents: 3,


                headerToolbar: {

                    left: "today prev,next",

                    center: "title",

                    right:
                        "dayGridMonth,timeGridWeek,timeGridDay"
                },


                buttonText: {

                    today: "Today",

                    month: "Month",

                    week: "Week",

                    day: "Day"
                },
                
                eventTimeFormat: {
                    hour: "numeric",
                    minute: "2-digit",
                    meridiem: "short"
                },

                events:
                    async function(
                        fetchInfo,
                        successCallback,
                        failureCallback
                    ) {

                        try {

                            const url =
                                `${API_URL}/calendar/events` +
                                `?start_datetime=${encodeURIComponent(fetchInfo.startStr)}` +
                                `&end_datetime=${encodeURIComponent(fetchInfo.endStr)}`;


                            const response =
                                await fetch(url);


                            if (!response.ok) {

                                throw new Error(
                                    `Calendar request failed: ${response.status}`
                                );
                            }


                            const events =
                                await response.json();


                            successCallback(events.map(event => ({
                                id: event.id,
                                title: event.title,
                                start: event.start,
                                end: event.end
                            })));

                        }

                        catch (error) {

                            console.error(
                                "Could not load Google Calendar:",
                                error
                            );

                            failureCallback(error);
                        }
                    },


                eventColor: "#cfc4f7",

                eventTextColor: "#34313a",

                eventDisplay: "block",

                dayMaxEventRows: true

            }
        );


    googleCalendar.render();
}


// ============================================================
// INITIALIZE
// ============================================================

initializeCalendar();

loadTasks();