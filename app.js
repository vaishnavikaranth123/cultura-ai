// ==================================================
// GLOBAL
// ==================================================

let selectedExperience = "AR";


// ==================================================
// HELPERS
// ==================================================

function get(id) {

    return document.getElementById(id);

}


function escapeHTML(value) {

    return String(value ?? "")

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");

}


function speak(text) {

    if (!text) {
        return;
    }


    if (
        !window.speechSynthesis
    ) {

        alert(
            "Text-to-speech is not supported."
        );

        return;

    }


    window.speechSynthesis.cancel();


    const utterance =
        new SpeechSynthesisUtterance(
            text
        );


    utterance.rate =
        0.9;


    window.speechSynthesis.speak(
        utterance
    );

}


function stopSpeaking() {

    if (
        window.speechSynthesis
    ) {

        window.speechSynthesis.cancel();

    }

}


// ==================================================
// LOAD CREATORS
// ==================================================

async function loadCreators() {

    try {

        const response =
            await fetch(
                "/api/creators/"
            );


        const data =
            await response.json();


        const grid =
            get("creatorGrid");


        grid.innerHTML = "";


        if (
            !data.creators ||
            data.creators.length === 0
        ) {

            grid.innerHTML = `
                <div class="creator-card">
                    <h3>No creators yet</h3>
                    <p>
                        Become the first creator on
                        the platform.
                    </p>
                </div>
            `;

            return;

        }


        data.creators.forEach(
            creator => {

                grid.innerHTML += `

                    <div class="creator-card">

                        <span class="badge">
                            ${escapeHTML(
                                creator.creator_type
                            )}
                        </span>

                        <h3>
                            ${escapeHTML(
                                creator.name
                            )}
                        </h3>

                        <p>
                            ${escapeHTML(
                                creator.region
                            )}
                        </p>

                        <p>
                            ${escapeHTML(
                                creator.tradition
                            )}
                        </p>

                        <p>
                            ${escapeHTML(
                                creator.bio
                            )}
                        </p>

                    </div>
                `;

            }
        );

    }

    catch (error) {

        console.error(error);

    }

}


// ==================================================
// LOAD WORKS
// ==================================================

async function loadWorks() {

    try {

        const response =
            await fetch(
                "/api/works/"
            );


        const data =
            await response.json();


        const grid =
            get("worksGrid");


        grid.innerHTML = "";


        if (
            !data.works ||
            data.works.length === 0
        ) {

            grid.innerHTML = `
                <div class="work-card">
                    <h3>No works published yet</h3>
                    <p>
                        Published creative works
                        will appear here.
                    </p>
                </div>
            `;

            return;

        }


        data.works.forEach(
            work => {

                const image = work.image_path

                    ? `
                        <img
                            src="${escapeHTML(
                                work.image_path
                            )}"
                            alt=""
                        >
                    `

                    : "";


                grid.innerHTML += `

                    <div class="work-card">

                        ${image}

                        <span class="badge">
                            ${escapeHTML(
                                work.category
                            )}
                        </span>

                        <h3>
                            ${escapeHTML(
                                work.title
                            )}
                        </h3>

                        <p>
                            Creator:
                            ${escapeHTML(
                                work.creator_name
                            )}
                        </p>

                        <p>
                            ${escapeHTML(
                                work.creator_description
                            )}
                        </p>

                    </div>

                `;

            }
        );

    }

    catch (error) {

        console.error(error);

    }

}


// ==================================================
// CREATE CREATOR
// ==================================================

get("createCreatorBtn")
.addEventListener(
    "click",
    async function() {

        const body = {

            name:
                get("creatorName").value.trim(),

            creator_type:
                get("creatorType").value,

            region:
                get("creatorRegion").value.trim(),

            language:
                get("creatorLanguage").value.trim(),

            bio:
                get("creatorBio").value.trim(),

            tradition:
                get("creatorTradition").value.trim(),

            social_link:
                get("creatorSocial").value.trim()

        };


        if (!body.name) {

            get("creatorStatus")
            .textContent =
                "Enter creator name.";

            return;

        }


        try {

            const response =
                await fetch(
                    "/api/creators/",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Could not create creator."
                );

            }


            get("creatorStatus")
            .textContent =
                `Creator created successfully. ID: ${data.creator_id}`;


            get("workCreatorId").value =
                data.creator_id;


            loadCreators();

        }

        catch (error) {

            get("creatorStatus")
            .textContent =
                "Error: " + error.message;

        }

    }
);


// ==================================================
// PUBLISH WORK
// ==================================================

get("publishWorkBtn")
.addEventListener(
    "click",
    async function() {

        const creatorId =
            get("workCreatorId").value;


        const title =
            get("workTitle").value.trim();


        if (
            !creatorId ||
            !title
        ) {

            get("workStatus")
            .textContent =
                "Creator ID and work title are required.";

            return;

        }


        const formData =
            new FormData();


        formData.append(
            "creator_id",
            creatorId
        );


        formData.append(
            "title",
            title
        );


        formData.append(
            "category",
            get("workCategory").value
        );


        formData.append(
            "creator_description",
            get("creatorDescription").value
        );


        formData.append(
            "cultural_context",
            get("culturalContext").value
        );


        formData.append(
            "tags",
            get("workTags").value
        );


        const file =
            get("workImage").files[0];


        if (file) {

            formData.append(
                "image",
                file
            );

        }


        try {

            const response =
                await fetch(
                    "/api/works/create",
                    {

                        method: "POST",

                        body: formData

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Could not publish work."
                );

            }


            get("workStatus")
            .textContent =
                "✓ Work published successfully.";


            loadWorks();

        }

        catch (error) {

            get("workStatus")
            .textContent =
                "Error: " + error.message;

        }

    }
);


// ==================================================
// STORY
// ==================================================

get("generateStoryBtn")
.addEventListener(
    "click",
    async function() {

        get("storyResult")
        .textContent =
            "Gemini is creating the story presentation...";


        const body = {

            creator_name:
                get("storyCreator").value,

            work_title:
                get("storyWork").value,

            creator_description:
                get("storyDescription").value,

            cultural_context:
                get("storyContext").value,

            audience:
                "general public",

            language:
                get("storyLanguage").value,

            style:
                "human-centered cultural story"

        };


        try {

            const response =
                await fetch(
                    "/api/stories/generate",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Story generation failed."
                );

            }


            get("storyResult")
            .textContent =
                data.story;


            get("storyListen")
            .disabled =
                false;

        }

        catch (error) {

            get("storyResult")
            .textContent =
                "Error: " + error.message;

        }

    }
);


// ==================================================
// STORY AUDIO
// ==================================================

get("storyListen")
.addEventListener(
    "click",
    function() {

        speak(
            get("storyResult")
            .textContent
        );

    }
);


get("storyStop")
.addEventListener(
    "click",
    function() {

        stopSpeaking();

    }
);


// ==================================================
// ACCESSIBILITY
// ==================================================

get("accessBtn")
.addEventListener(
    "click",
    async function() {

        const content =
            get("accessContent").value;


        if (!content.trim()) {

            get("accessResult")
            .textContent =
                "Enter creator/work content first.";

            return;

        }


        get("accessResult")
        .textContent =
            "Creating accessibility description...";


        try {

            const response =
                await fetch(
                    "/api/accessibility/generate",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({

                                content,

                                language:
                                    get("accessLanguage").value

                            })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Accessibility generation failed."
                );

            }


            get("accessResult")
            .textContent =
                data.description;


            get("accessListen")
            .disabled =
                false;

        }

        catch (error) {

            get("accessResult")
            .textContent =
                "Error: " + error.message;

        }

    }
);


// ==================================================
// ACCESSIBILITY AUDIO
// ==================================================

get("accessListen")
.addEventListener(
    "click",
    function() {

        speak(
            get("accessResult")
            .textContent
        );

    }
);


// ==================================================
// EXPERIENCE TYPE
// ==================================================

document
    .querySelectorAll(
        ".experience-card"
    )
    .forEach(
        card => {

            card.addEventListener(
                "click",
                function() {

                    document
                        .querySelectorAll(
                            ".experience-card"
                        )
                        .forEach(
                            item => {

                                item.classList
                                    .remove(
                                        "active"
                                    );

                            }
                        );


                    card.classList.add(
                        "active"
                    );


                    selectedExperience =
                        card.dataset.type;

                }
            );

        }
    );


// ==================================================
// IMMERSIVE EXPERIENCE
// ==================================================

get("immersiveBtn")
.addEventListener(
    "click",
    async function() {

        get("immersiveResult")
        .textContent =
            `Designing ${selectedExperience} experience...`;


        const body = {

            creator_name:
                get("immersiveCreator").value,

            work_title:
                get("immersiveWork").value,

            creator_description:
                get("immersiveDescription").value,

            cultural_context:
                get("immersiveContext").value,

            experience_type:
                selectedExperience,

            audience:
                "general public"

        };


        try {

            const response =
                await fetch(
                    "/api/immersive/generate",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Experience generation failed."
                );

            }


            get("immersiveResult")
            .textContent =
                data.experience;

        }

        catch (error) {

            get("immersiveResult")
            .textContent =
                "Error: " + error.message;

        }

    }
);


// ==================================================
// RESEARCH
// ==================================================

get("researchBtn")
.addEventListener(
    "click",
    async function() {

        get("researchResult")
        .textContent =
            "Preparing preservation and research plan...";


        const body = {

            creator_name:
                get("researchCreator").value,

            work_title:
                get("researchWork").value,

            creator_description:
                get("researchDescription").value,

            cultural_context:
                get("researchContext").value

        };


        try {

            const response =
                await fetch(
                    "/api/research/generate",
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Research generation failed."
                );

            }


            get("researchResult")
            .textContent =
                data.research_plan;

        }

        catch (error) {

            get("researchResult")
            .textContent =
                "Error: " + error.message;

        }

    }
);


// ==================================================
// INITIAL LOAD
// ==================================================

loadCreators();

loadWorks();