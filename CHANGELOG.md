## Nova Galaxy 0.9.1
- Added `get_full_status` method to tool in order to get detailed messages mostly for error states (thanks to Gregory Cage). [Merge Request 23](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/23)

### Nova Galaxy 0.9.0
- When uploading datasets with manually set content, the upstream name will mirror the local name property of the dataset (thanks to Gregory Cage). [Merge Request 22](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/22)
- New WorkStates for the actual process of stopping and canceling jobs (separate from the terminal states already present) (thanks to Sergey Yakubov and Gregory Cage). [Merge Request 22](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/22)
- Fixed major bug where tools were not being stopped and fetching results properly (canceling worked fine) (thanks to Gregory Cage). [Merge Request 22](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/22)
- Made tool status thread safe (thanks to Sergey Yakubov and Gregory Cage). [Merge Request 22](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/22)
- If canceling or stopping jobs in the uploading data state, will stop the uploading when able (thanks to Sergey Yakubov and Gregory Cage). [Merge Request 22](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/22)
- Misc backend code cleanup (thanks to Sergey Yakubov and Gregory Cage). [Merge Request 22](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/22)

### Nova Galaxy, 0.8.2
- Now returns file type automatically if available (thanks to Gregory Cage). [Merge Request 21](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/21)
- Returns file content as bytes instead of string (thanks to Gregory Cage). [Merge Request 21](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/21)


### Nova Galaxy, 0.8.1
- Can now fetch specific stdout and stderr positions and length (thanks to Gregory Cage). [Merge Request 19](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/19)

### Nova Galaxy, 0.8.0
- `get_data_store()` has been added to the ConnectionHelper class. This functionally does the same thing as create_data_store, but users can choose whether to only use existing upstream data stores. `create_data_store` creates data stores by default and connects to existing ones as well automatically (thanks to Gregory Cage).  [Merge Request 18](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/18)
- `Connections.connect()` can now be used with or without the `with` keyword. Consequently, stores can also be created outside a `with` block. `Connection.close()` performs the clean up that exiting the `with` block provides (thanks to Gregory Cage). [Merge Request 18](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/18)
- Data stores can be cleaned up manually (thanks to Gregory Cage). [Merge Request 18](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/18)
- Can now wait for the result of a running tool (thanks to Gregory Cage). [Merge Request 18](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/18)

### Nova Galaxy, 0.7.4
- Allow users to choose to check URL when calling get_url() from a Tool (thanks to Gregory Cage). [Merge Request 17](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/17)
- Return more detailed information when getting the content of a DatasetCollection (thanks to Gregory Cage). [Merge Request 17](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/17)
- Data stores are now persisted by default. A new mark_for_cleanup method has been provided to clean up data stores after usage. The persist method's behavior remains unchanged (thanks to Gregory Cage). [Merge Request 17](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/17)

### Nova Galaxy, 0.7.3
- Allow Dataset content to be set manually in memory rather than only loading from a file or downloading from Galaxy (thanks to Gregory Cage). [Merge Request 16](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/16)
- Add file type (extensions) to Datasets (thanks to Gregory Cage). [Merge Request 16](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/16)

### Nova Galaxy, 0.7.2
- Add more states to Work State enum (thanks to Gregory Cage). [Merge Request 15](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/15)

### Nova Galaxy, 0.7.1
- Speeds ups recovering tools from data stores. (thanks to Gregory Cage). [Merge Request 14](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/14)

### Nova Galaxy, 0.7.0
- Reworks some issues where the url was trying to be fetched in scenarios where it would take the full timeout (thanks to Gregory Cage).  [Merge Request 13](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/13)
- Added a lot more user documentation (thanks to Gregory Cage).  [Merge Request 13](https://code.ornl.gov/ndip/public-packages/nova-galaxy/-/merge_requests/13)
- Changed the Workstate enum to have string values (much more useful when trying to serialize the value) (thanks to Gregory Cage).  [Merge Request 13](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/13)
- Changes Nova class name to Connection, and NovaConnection to ConnectionHelper (thanks to Gregory Cage).  [Merge Request 13](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/13)

### Nova Galaxy, 0.6.1
- Fix dictionary bug with data stores (thanks to Gregory Cage). [Merge Request 12](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/12)

### Nova Galaxy, 0.6.0
- Add recovery for data stores (thanks to Gregory Cage). [Merge Request 10](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/10)
- Add IDs to tools (thanks to Gregory Cage). [Merge Request 10](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/10)
- Reworked back end infrastructure for managing tool execution. (thanks to Gregory Cage). [Merge Request 8](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/8)
- Add readthedocs support (thanks to Andrew Ayres). [Merge Request 5](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/5)
- Add initial testing for library (thanks to Gregory Cage). [Merge Request 3](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/3)
- Set up read the docs for package (thanks to Andrew Ayres). [Merge Request 4](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/4)
- Add interactive tool execution (thanks to Gregory Cage). [Merge Request 2](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/2)
- Initial implementation of nova library (thanks to Gregory Cage). [Merge Request 1](https://code.ornl.gov/ndip/public-packages/ndip-galaxy/-/merge_requests/1)
