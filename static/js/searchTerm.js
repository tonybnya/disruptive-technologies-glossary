const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const resultsContainer = document.getElementById("results");

const performSearch = async () => {
  const searchTerm = searchInput.value.trim().toLowerCase();
  if (!searchInput || searchTerm === "") {
    alert("Veuillez entrer un terme pour effectuer une recherche.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5003/api/terms");
    const data = await response.json();
    // console.log(data);

    const filteredResults = data.filter(
      (item) =>
        item.french_term.toLowerCase().includes(searchTerm) ||
        item.english_term.toLowerCase().includes(searchTerm),
    );

    displayResults(filteredResults);
  } catch (error) {
    alert("Vérifiez l'orthographe du terme et Réessayez !");
    console.error("Error fetching data:", error);
    resultsContainer.innerHTML = `<p>Erreur dans l'obtention des résultats. Veuillez réessayer.</p>`;
  }
};

searchButton.addEventListener("click", performSearch);
searchInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    performSearch();
  }
});

const displayResults = (results) => {
  if (results.length === 0) {
    resultsContainer.innerHTML = "<p>Aucun résultat trouvé.</p>";
    return;
  }

  resultsContainer.innerHTML = results
    .map(
      (item) => `
<div class="bg-white shadow-lg rounded-lg mb-4 p-4 sm:p-6 h-full max-w-full">
  <div class="flex flex-col items-start gap-1 mb-4">
    <h3 class="text-xl max-sm:text-lg font-bold leading-none text-gray-500">
      <span class="text-[#A32A34] font-bold">${item.english_term}</span>
    </h3>
    <h4 class="text-gray-700">
      <span class="text-[#296F9A] font-bold">SL</span>: ${item.semantic_label_en}
    </h4>
    <h4 class="text-gray-700">
      Domain:
      <span class="text-[#296F9A] font-bold">${item.domain_en}</span>
    </h4>
    <h4 class="text-gray-700">
      Subdomain:
      ${displaySubdomains("Sous-domaine", item.subdomains_en)}
    </h4>
  </div>
  <div class="flow-root">
    <ul role="list" class="divide-y divide-gray-200">
      ${displayIfExists("Variant", item.variant_en)}
      ${displayIfExists("Synonym", item.near_synonym_en)}
      ${displayIfExists("Definition", item.definition_en)}
      ${displayCooccurrenceIfExists("Syntactic Cooccurrence", item.syntactic_cooccurrence_en)}
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-lg text-[#296F9A] font-bold">Lexical Relations</p>
            ${displayLexicalRelations(item.lexical_relations_en)}
          </div>
        </div>
      </li>
      ${displayIfExists("Note", item.note_en)}
      ${displayIfExists("Not to be confused with", item.note_to_be_confused_with_en)}
      ${displayIfExists("Frequent expression", item.frequent_expression_en)}
      ${displayIfExists("Phraseology", item.phraseology_en)}
      <li class="pt-3 sm:pt-4 pb-0">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-lg text-[#296F9A] font-bold">Context</p>
            <p class="text-md font-medium text-gray-900">${item.context_en}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</div>
<!---->
<div class="bg-white shadow-lg rounded-lg mb-4 p-4 sm:p-6 h-full">
  <div class="flex flex-col items-start gap-1 mb-4">
    <h3 class="text-xl max-sm:text-lg font-bold leading-none text-gray-500">
      <span class="text-[#A32A34] font-bold">${item.french_term}</span>
    </h3>
    <h4 class="text-gray-700">
      <span class="text-[#296F9A] font-bold">ES</span>: ${item.semantic_label_fr}
    </h4>
    <h4 class="text-gray-700">
      Domaine :
      <span class="text-[#296F9A] font-bold">${item.domain_fr}</span>
    </h4>
    <h4 class="">
      Sous-domaine :
      ${displaySubdomains("Sous-domaine", item.subdomains_fr)}
    </h4>
  </div>
  <div class="flow-root">
    <ul role="list" class="divide-y divide-gray-200">
      ${displayIfExists("Variante", item.variant_fr)}
      ${displayIfExists("Synonyme", item.near_synonym_fr)}
      ${displayIfExists("Définition", item.definition_fr)}
      ${displayCooccurrenceIfExists("Cooccurrence Syntaxique", item.syntactic_cooccurrence_fr)}
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-lg text-[#296F9A] font-bold">Relations lexicales</p>
            ${displayLexicalRelations(item.lexical_relations_fr)}
          </div>
        </div>
      </li>
      ${displayIfExists("Note", item.note_fr)}
      ${displayIfExists("À ne pas confondre avec", item.note_to_be_confused_with_fr)}
      ${displayIfExists("Expression fréquente", item.frequent_expression_fr)}
      ${displayIfExists("Phraséologie", item.phraseology_fr)}
      <li class="pt-3 sm:pt-4 pb-0">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-lg text-[#296F9A] font-bold">Contexte</p>
            <p class="text-md font-medium text-gray-900">${item.context_fr}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</div>
`,
    )
    .join("");

  document.getElementById("search-input").value = "";
};

const displayIfExists = (label, value) => {
  if (value && value.trim() !== "") {
    return `
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-lg text-[#296F9A] font-bold">${label}</p>
            <p class="text-sm font-medium text-gray-900">${value}</p>
          </div>
        </div>
      </li>`;
  }
  return "";
};

const displaySubdomains = (label, subdomains) => {
  const colors = [
    { text: "text-white", bg: "bg-[#296F9A]" },
    { text: "text-white", bg: "bg-[#A32A34]" },
    { text: "text-white", bg: "bg-black" },
  ];

  return subdomains
    .map((item, index) => {
      const color = colors[index % colors.length];
      return `
        <span class="inline-block ${color.bg} ${color.text} py-1 px-2 mr-1 mb-2 rounded-lg text-sm">${item}</span>
      `;
    })
    .join("");
};

const displayCooccurrence = (label, cooccurrence) => {
  if (Array.isArray(cooccurrence) && cooccurrence.length > 0) {
    return cooccurrence
      .map((item, index) => {
        return `
      <span class="mb-0 text-sm">${item || "<br />"}</span>
      `;
      })
      .join("");
  }
  return "";
};

const displayCooccurrenceIfExists = (label, cooccurrence) => {
  if (Array.isArray(cooccurrence) && cooccurrence.length > 0) {
    const formattedItems = cooccurrence
      .map(item => `<span class="mb-0 text-sm">${item || "<br />"}</span>`)
      .join("");

    return `
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex flex-col min-w-0">
            <p class="text-lg text-[#296F9A] font-bold">${label}</p>
            ${formattedItems}
          </div>
        </div>
      </li>
    `;
  }
  return "";
};

const displayLexicalRelations = (lexicalRelations) => {
  let html =
    '<table class="table-auto text-sm w-full text-left whitespace-normal">';

  lexicalRelations.forEach((relation) => {
    const key = Object.keys(relation)[0];
    const values = relation[key];
    html += `<tr>`;
    html += `<th class="pl-0 py-2 font-bold">${key}</th>`;
    html += `<td class="pl-0 py-2 text-sm">`;
    if (Array.isArray(values)) {
      html += values.join("<br>");
    } else if (values) {
      html += values;
    } else {
      html += "";
    }
    html += `</td>`;
    html += `</tr>`;
  });

  html += "</table>";
  return html;
};