import json

def summarize_galaxy_tools(input_filepath="tools.json", 
                           output_json_filepath="tools_summary.json", 
                           output_txt_filepath="tools_summary.txt"):
    """
    Summarizes a Galaxy tools JSON file.
    """
    try:
        with open(input_filepath, 'r') as f:
            tool_sections = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_filepath}'")
        return

    summarized_sections = []
    section_tool_counts = {}
    total_tool_count = 0

    for section in tool_sections:

        if section.get("model_class") != "ToolSection" or "elems" not in section:
            continue

        section_name = section.get("name", "Unnamed Section")
        summarized_section = {
            "name": section_name,
            "description": section.get("description"),
            "elems": []
        }

        tool_count_in_section = 0
        for tool in section["elems"]:
            # Consider elements with a 'name' and 'description' as tools for this summary
            if "name" in tool and "description" in tool:
                summarized_tool = {
                    "name": tool.get("name"),
                    "description": tool.get("description"),
                    "is_workflow_compatible": tool.get("is_workflow_compatible"),
                    "target": tool.get("target"),
                    "model_class": tool.get("model_class")
                }
                summarized_section["elems"].append(summarized_tool)
                tool_count_in_section += 1
        
        summarized_sections.append(summarized_section)
        section_tool_counts[section_name] = tool_count_in_section
        total_tool_count += tool_count_in_section

    # Write the summarized JSON output
    with open(output_json_filepath, 'w') as f:
        json.dump(summarized_sections, f, indent=4)
    print(f"Successfully created summarized JSON file: {output_json_filepath}")

    # Write the text summary
    with open(output_txt_filepath, 'w') as f:
        f.write("Galaxy Tools Summary\n")
        f.write("====================\n\n")
        f.write("Tool count per section:\n")
        for name, count in section_tool_counts.items():
            f.write(f"- {name}: {count}\n")
        
        f.write("\n--------------------\n")
        f.write(f"Total number of tools: {total_tool_count}\n")
    print(f"Successfully created summary report: {output_txt_filepath}")


if __name__ == "__main__":
    summarize_galaxy_tools(input_filepath="tools.json")