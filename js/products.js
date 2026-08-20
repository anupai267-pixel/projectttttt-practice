// ========================================
// EcoFinds Products JavaScript
// ========================================


// Get product cards

const productCards =
    Array.from(
        document.querySelectorAll(".marketplace-card")
    );

const productSearch =
    document.getElementById("productSearch");

const categoryFilter =
    document.getElementById("categoryFilter");

const conditionFilter =
    document.getElementById("conditionFilter");

const minPrice =
    document.getElementById("minPrice");

const maxPrice =
    document.getElementById("maxPrice");

const locationFilter =
    document.getElementById("locationFilter");

const ecoFilter =
    document.getElementById("ecoFilter");

const ecoValue =
    document.getElementById("ecoValue");

const applyFilters =
    document.getElementById("applyFilters");

const clearFilters =
    document.getElementById("clearFilters");

const sortProducts =
    document.getElementById("sortProducts");

const productCount =
    document.getElementById("productCount");

const productsGrid =
    document.getElementById("productsGrid");

const emptyProducts =
    document.getElementById("emptyProducts");


// ========================================
// ECO RANGE
// ========================================

if (ecoFilter) {

    ecoFilter.addEventListener("input", function () {

        ecoValue.textContent =
            ecoFilter.value + "+";

    });

}


// ========================================
// FILTER PRODUCTS
// ========================================

function filterProducts() {

    const search =
        productSearch.value
            .trim()
            .toLowerCase();

    const category =
        categoryFilter.value;

    const condition =
        conditionFilter.value;

    const minimum =
        minPrice.value === ""
            ? 0
            : Number(minPrice.value);

    const maximum =
        maxPrice.value === ""
            ? Infinity
            : Number(maxPrice.value);

    const location =
        locationFilter.value
            .trim()
            .toLowerCase();

    const minimumEco =
        Number(ecoFilter.value);


    let visibleProducts = 0;


    productCards.forEach(function (card) {

        const name =
            card.dataset.name.toLowerCase();

        const cardCategory =
            card.dataset.category;

        const cardCondition =
            card.dataset.condition;

        const price =
            Number(card.dataset.price);

        const cardLocation =
            card.dataset.location.toLowerCase();

        const eco =
            Number(card.dataset.eco);


        const matchesSearch =
            search === "" ||
            name.includes(search);


        const matchesCategory =
            category === "all" ||
            cardCategory === category;


        const matchesCondition =
            condition === "all" ||
            cardCondition === condition;


        const matchesPrice =
            price >= minimum &&
            price <= maximum;


        const matchesLocation =
            location === "" ||
            cardLocation.includes(location);


        const matchesEco =
            eco >= minimumEco;


        const shouldShow =
            matchesSearch &&
            matchesCategory &&
            matchesCondition &&
            matchesPrice &&
            matchesLocation &&
            matchesEco;


        if (shouldShow) {

            card.style.display = "";

            visibleProducts++;

        } else {

            card.style.display = "none";

        }

    });


    updateProductCount(visibleProducts);


    if (visibleProducts === 0) {

        emptyProducts.classList.add("show");

    } else {

        emptyProducts.classList.remove("show");

    }

}


// ========================================
// APPLY FILTER
// ========================================

if (applyFilters) {

    applyFilters.addEventListener(
        "click",
        filterProducts
    );

}


// ========================================
// LIVE SEARCH
// ========================================

if (productSearch) {

    productSearch.addEventListener(
        "input",
        filterProducts
    );

}


// ========================================
// SORT
// ========================================

if (sortProducts) {

    sortProducts.addEventListener(
        "change",
        function () {

            const value =
                sortProducts.value;


            const cards =
                Array.from(
                    productsGrid.querySelectorAll(
                        ".marketplace-card"
                    )
                );


            cards.sort(function (a, b) {

                const priceA =
                    Number(a.dataset.price);

                const priceB =
                    Number(b.dataset.price);

                const ecoA =
                    Number(a.dataset.eco);

                const ecoB =
                    Number(b.dataset.eco);


                if (value === "low") {

                    return priceA - priceB;

                }


                if (value === "high") {

                    return priceB - priceA;

                }


                if (value === "eco") {

                    return ecoB - ecoA;

                }


                // Newest
                // Temporary order because backend
                // will later provide created_at.

                return 0;

            });


            cards.forEach(function (card) {

                productsGrid.appendChild(card);

            });

        }

    );

}


// ========================================
// CLEAR FILTERS
// ========================================

if (clearFilters) {

    clearFilters.addEventListener(
        "click",
        function () {

            productSearch.value = "";

            categoryFilter.value = "all";

            conditionFilter.value = "all";

            minPrice.value = "";

            maxPrice.value = "";

            locationFilter.value = "";

            ecoFilter.value = 0;

            ecoValue.textContent = "0+";


            filterProducts();

        }
    );

}


// ========================================
// UPDATE COUNT
// ========================================

function updateProductCount(count) {

    if (productCount) {

        productCount.textContent =
            count + (count === 1
                ? " Product"
                : " Products");

    }

}


// ========================================
// URL SEARCH
// ========================================

function loadSearchFromURL() {

    const params =
        new URLSearchParams(
            window.location.search
        );


    const search =
        params.get("search");

    const category =
        params.get("category");


    if (search && productSearch) {

        productSearch.value = search;

    }


    if (category && categoryFilter) {

        categoryFilter.value = category;

    }


    if (search || category) {

        filterProducts();

    }

}


loadSearchFromURL();