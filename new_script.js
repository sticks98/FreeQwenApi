        // Замена LaTeX формул - конвертируем [] и () скобки в $ для inline форматирования MathJax
        function replaceLatex(text) {
            // Заменяем формулы в квадратных скобках [...] на $...$ для inline форматирования
            text = text.replace(/\[/g, '\\\\(');
            text = text.replace(/\]/g, '\\\\)');
            // Заменяем формулы в круглых скобках (...) на $...$ для inline форматирования
            text = text.replace(/\(/g, '\\\\(');
            text = text.replace(/\)/g, '\\\\)');
            // Также поддерживаем старые форматы $...$ и $$...$$
            text = text.replace(/\$\$(.*?)\$\$/g, '\\\\[$1\\\\]');
            text = text.replace(/\$(.*?)\$/g, '\\\\($1\\\\)');
            return text;
        }
