from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring


@magics_class
class DCSMagics(Magics):
    """
    A class for DCS-related magic commands.
    """

    @magic_arguments()
    @argument("--topic", type=str, default=None, help="Filter frameworks by topic.")
    @line_magic
    def dcs_frameworks(self, line: str):
        """
        Magic command to list available DCS frameworks.
        """
        args = parse_argstring(self.dcs_frameworks, line)

        # In a future implementation, this could be loaded dynamically from the
        # framework directory. For now, we hardcode the examples from the notebook.
        frameworks = {
            "populism": [
                "tamaki_fuks_competitive_populism - Brazilian political competition analysis",
                "populism_pluralism - Binary populist vs pluralist classification",
                "political_worldview_triad - Populism within broader worldview context",
            ],
            "ethics": ["business_ethics - For analyzing corporate discourse"],
        }

        topic = args.topic.lower() if args.topic else None

        if topic:
            print(f"Available frameworks for '{topic}':")
            if topic in frameworks:
                for i, fw in enumerate(frameworks[topic], 1):
                    print(f"{i}. {fw}")
            else:
                print(f"No frameworks found for topic: {topic}")
        else:
            print("Available frameworks:")
            for current_topic, fw_list in frameworks.items():
                print(f"\nTopic: {current_topic}")
                for i, fw in enumerate(fw_list, 1):
                    print(f"  {i}. {fw}")

        print("\nUsage: %dcs_apply tamaki_fuks_competitive_populism")

    @cell_magic
    def dcs_framework(self, line: str, cell: str):
        """
        Cell magic to apply a DCS framework to data in the cell.
        
        Usage:
        %%dcs_framework tamaki_fuks
        data_variable_name
        """
        framework = line.strip()
        
        # Execute the cell content to get the data variable
        try:
            # Get the IPython instance
            ip = self.shell
            
            # Execute the cell content in the user namespace
            result = ip.run_cell(cell)
            
            # Try to find a DataFrame in the result
            if hasattr(result, 'result') and hasattr(result.result, 'dcs'):
                # If the cell returns a DataFrame directly
                df = result.result
                print(f"Applying {framework} framework...")
                viz = getattr(df.dcs, framework)()
                viz.plot()
            else:
                # Look for DataFrames in the user namespace from the cell
                user_ns = ip.user_ns
                dataframes = {name: obj for name, obj in user_ns.items() 
                             if hasattr(obj, 'dcs') and hasattr(obj, 'columns')}
                
                if dataframes:
                    # Use the first DataFrame found
                    df_name, df = next(iter(dataframes.items()))
                    print(f"Applying {framework} framework to {df_name}...")
                    viz = getattr(df.dcs, framework)()
                    viz.plot()
                else:
                    print("❌ No DataFrame with DCS accessor found in cell")
                    print("Make sure your cell contains a pandas DataFrame")
                    
        except Exception as e:
            print(f"❌ Error applying framework: {e}")
            print("Cell content:", cell.strip())


def load_ipython_extension(ipython):
    """
    This function is called when the extension is loaded.
    It registers the magics.
    """
    ipython.register_magics(DCSMagics) 